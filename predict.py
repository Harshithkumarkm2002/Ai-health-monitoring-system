import joblib
import pandas as pd

model = joblib.load("heart_model.pkl")

def predict_heart(data):

    input_df = pd.DataFrame([[
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
        data["thal"]
    ]], columns=[
        "age", "sex", "cp", "trestbps", "chol", "fbs",
        "restecg", "thalach", "exang", "oldpeak",
        "slope", "ca", "thal"
    ])

    prediction = model.predict(input_df)[0]

    if prediction == 0:
        return "⚠️ High Risk of Heart Disease"
    else:
        return "✅ Low Risk of Heart Disease"
