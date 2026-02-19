from google import genai
import os
from dotenv import load_dotenv


load_dotenv()

key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=key)

def generate_explanation(data, prediction):
    """
    Calls Gemini and returns structured explanation
    """

    prompt = f"""
You are a medical AI assistant.

Patient Data:
Age: {data['age']}
Cholesterol: {data['chol']}
Resting BP: {data['trestbps']}
Max Heart Rate: {data['thalach']}
Exercise Angina: {data['exang']}

Prediction: {prediction}

Respond ONLY in the following EXACT format:

Risk Summary:
<one short paragraph>

Possible Reasons:
- reason 1
- reason 2
- reason 3

Lifestyle Suggestions:
- suggestion 1
- suggestion 2
- suggestion 3

Medical Disclaimer:
<one short sentence>
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    structured_explanation = parse_explanation(response.text)

    return structured_explanation


def parse_explanation(text):
    """
    Converts Gemini raw text into structured dictionary
    """

    sections = {
        "risk_summary": "",
        "reasons": [],
        "suggestions": [],
        "disclaimer": ""
    }

    current_section = None

    for line in text.split("\n"):
        line = line.strip()

        if not line:
            continue

        if line.startswith("Risk Summary:"):
            current_section = "risk_summary"
            continue

        if line.startswith("Possible Reasons:"):
            current_section = "reasons"
            continue

        if line.startswith("Lifestyle Suggestions:"):
            current_section = "suggestions"
            continue

        if line.startswith("Medical Disclaimer:"):
            current_section = "disclaimer"
            continue

        if current_section == "risk_summary":
            sections["risk_summary"] += line + " "

        elif current_section == "reasons" and line.startswith("-"):
            sections["reasons"].append(line[1:].strip())

        elif current_section == "suggestions" and line.startswith("-"):
            sections["suggestions"].append(line[1:].strip())

        elif current_section == "disclaimer":
            sections["disclaimer"] += line + " "

    return sections

