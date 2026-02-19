# Heart Disease Prediction System

A full-stack AI web application for predicting heart disease risk using a trained machine learning model, enhanced with LLM-based medical explanations and persistent user history.

---

## Overview

This project is a production-style AI system that allows authenticated users to input medical parameters and receive a heart disease risk prediction along with a structured, human-readable AI explanation. All predictions are securely stored and can be reviewed later.

The system integrates Machine Learning, Flask, MySQL, and Google Gemini (LLM).

---

## Key Features

- Google OAuth-based authentication  
- Heart disease prediction using a trained ML model  
- AI-generated medical explanation using Google Gemini  
- Structured explanation (summary, reasons, suggestions, disclaimer)  
- User-specific prediction history  
- Responsive UI with dark and light mode  

---

## Technology Stack

### Frontend
- HTML5
- CSS3
- Bootstrap
- Jinja2

### Backend
- Python
- Flask

### Machine Learning
- Scikit-learn
- Serialized model (`.pkl`)

### LLM
- Google Gemini (`google.genai`)

### Database
- MySQL

---

## Project Structure

heart-disease-prediction/
│
├── app.py # Flask application
├── predict.py # ML prediction logic
├── llm.py # Gemini LLM integration
├── heart_model.pkl # Trained ML model
├── requirements.txt
│
├── templates/
│ ├── home.html
│ ├── login.html
│ ├── predict.html
│ ├── result.html
│ └── history.html
│
└── README.md


---

## Input Features

| Feature | Description |
|-------|-------------|
| age | Age of patient |
| sex | 1 = Male, 0 = Female |
| cp | Chest pain type |
| trestbps | Resting blood pressure |
| chol | Serum cholesterol |
| fbs | Fasting blood sugar |
| restecg | Resting ECG result |
| thalach | Maximum heart rate |
| exang | Exercise-induced angina |
| oldpeak | ST depression |
| slope | Slope of ST segment |
| ca | Number of major vessels |
| thal | Thalassemia test result |

---

## Thalassemia (`thal`) Encoding

| Value | Meaning |
|------|--------|
| 1 | Normal |
| 2 | Fixed defect |
| 3 | Reversible defect |

Higher values indicate higher cardiac risk.

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/heart-disease-prediction.git
cd heart-disease-prediction

2. Create Virtual Environment

python -m venv venv
venv\Scripts\activate

3. Install Dependencies

pip install -r requirements.txt

Environment Variables

Set the following environment variables:

GEMINI_API_KEY=your_gemini_api_key
FLASK_SECRET_KEY=your_secret_key

CREATE DATABASE heart_app;
USE heart_app;

CREATE TABLE predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_email VARCHAR(255),
    age INT,
    sex INT,
    cp INT,
    trestbps INT,
    chol INT,
    fbs INT,
    restecg INT,
    thalach INT,
    exang INT,
    oldpeak FLOAT,
    slope INT,
    ca INT,
    thal INT,
    result VARCHAR(50),
    summary LONGTEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

Running the Application

python app.py

AI Explanation Pipeline

ML model predicts heart disease risk

Input data and prediction are sent to Gemini

Gemini returns a structured explanation

Explanation is parsed into:

Risk Summary

Possible Reasons

Lifestyle Suggestions

Medical Disclaimer

Explanation is stored as JSON in MySQL

Rendered cleanly on Result and History pages

Disclaimer

This project is for educational and demonstration purposes only.
It does not provide medical advice or diagnosis.