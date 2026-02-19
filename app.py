from flask import Flask, redirect, url_for, session, render_template , request
from authlib.integrations.flask_client import OAuth
from db_config import get_db_connection
from llm import generate_explanation
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
app.secret_key = "super_secret_key"

oauth = OAuth(app)

google = oauth.register(
    name='google',
    client_id= os.getenv("client_id"),
    client_secret=os.getenv("client_secret"),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login_page")
def login_page():
    return render_template("login.html")

@app.route("/login")
def login():
    return google.authorize_redirect(url_for('callback', _external=True))

@app.route("/callback")
def callback():
    token = google.authorize_access_token()
    

    resp = google.get("https://openidconnect.googleapis.com/v1/userinfo")

    user_info = resp.json()

    session['user'] = user_info
    
    return redirect(url_for("predict"))

from predict import predict_heart

import json

@app.route("/predict", methods=["GET", "POST"])
def predict():

    if 'user' not in session:
        return redirect(url_for("home"))

    if request.method == "POST":

        data = {
            "age": int(request.form["age"]),
            "sex": int(request.form["sex"]),
            "cp": int(request.form["cp"]),
            "trestbps": int(request.form["trestbps"]),
            "chol": int(request.form["chol"]),
            "fbs": int(request.form["fbs"]),
            "restecg": int(request.form["restecg"]),
            "thalach": int(request.form["thalach"]),
            "exang": int(request.form["exang"]),
            "oldpeak": float(request.form["oldpeak"]),
            "slope": int(request.form["slope"]),
            "ca": int(request.form["ca"]),
            "thal": int(request.form["thal"])
        }

        result = predict_heart(data)
        explanation = generate_explanation(data, result)

        session["prediction"] = result
        session["explanation"] = explanation

        explanation_json = json.dumps(explanation)

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO predictions (
                user_email, age, sex, cp, trestbps, chol, fbs,
                restecg, thalach, exang, oldpeak, slope, ca, thal,
                result, summary
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            session['user']['email'],
            data["age"],
            data["sex"],
            data["cp"],
            data["trestbps"],
            data["chol"],
            data["fbs"],
            data["restecg"],
            data["thalach"],
            data["exang"],
            data["oldpeak"],
            data["slope"],
            data["ca"],
            data["thal"],
            result,
            explanation_json   
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for("result"))

    return render_template(
        "predict.html",
        email=session['user']['email']
    )


@app.route("/result")
def result():
    if 'user' not in session:
        return redirect(url_for("home"))
    
    prediction = session.get("prediction")
    explanation = session.get("explanation")

    return render_template("result.html",
    prediction= prediction,
    explanation=explanation,
    email = session['user']['email']
    )

@app.route("/history")
def history():

    if 'user' not in session:
        return redirect(url_for("home"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM predictions
        WHERE user_email = %s
        ORDER BY created_at DESC
    """, (session['user']['email'],))

    records = cursor.fetchall()
    for r in records:
        try:
            summary = json.loads(r["summary"])
            r["explanation_html"] = summary.get("html", r["summary"])
        except:
            r["explanation_html"] = r["summary"]

    cursor.close()
    conn.close()

    return render_template("history.html",
                           records=records,
                           email=session['user']['email'])


@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
