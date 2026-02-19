import joblib
import pandas as pd

model = joblib.load("heart_model.pkl")

test_data = pd.DataFrame([
   
    [52, 1, 2, 135, 240, 0, 1, 150, 0, 1.2, 1, 1, 2]

], columns=[
    "age", "sex", "cp", "trestbps", "chol", "fbs",
    "restecg", "thalach", "exang", "oldpeak",
    "slope", "ca", "thal"
])

print(model.predict(test_data))
print(model.predict_proba(test_data))



