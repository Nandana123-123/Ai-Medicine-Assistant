# ai_service.py
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_default_medicine_response() -> dict:
    """Default response when AI fails"""
    return {
        "medicine_name": "Unknown Medicine",
        "generic_name": "Not identified",
        "category": "Unknown",
        "uses": "Could not identify. Please consult a pharmacist.",
        "advantages": "Please consult a doctor.",
        "side_effects": "Unknown - consult your doctor",
        "dosage": "Follow doctor's prescription",
        "age_group": "Consult doctor",
        "warnings": "Always consult a doctor before taking medicine",
        "storage": "Store in cool dry place",
        "when_to_see_doctor": "If unsure, always see a doctor",
        "simple_explanation": "We could not read this medicine. Show it to a pharmacist."
    }


def identify_medicine(ocr_text: str) -> dict:
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a medical assistant. Reply with valid JSON only."
                },
                {
                    "role": "user",
                    "content": f"""Based on this medicine text: "{ocr_text}"

Return this exact JSON:
{{
    "medicine_name": "name here",
    "generic_name": "generic name",
    "category": "type of medicine",
    "uses": "what it treats",
    "advantages": "benefits",
    "side_effects": "side effects",
    "dosage": "how much to take",
    "age_group": "suitable age",
    "warnings": "warnings",
    "storage": "storage info",
    "when_to_see_doctor": "when to see doctor",
    "simple_explanation": "simple explanation"
}}"""
                }
            ],
            max_tokens=1000
        )

        result = response.choices[0].message.content.strip()
        if "```" in result:
            result = result.split("```")[1]
            if result.startswith("json"):
                result = result[4:]
        return json.loads(result.strip())

    except Exception as e:
        print(f"AI error: {str(e)}")
        return get_default_medicine_response()


def simplify_for_uneducated_user(medicine_data: dict) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": f"Explain simply in 3 sentences for uneducated users. Medicine: {medicine_data.get('medicine_name')}, Uses: {medicine_data.get('uses')}"
                }
            ],
            max_tokens=150
        )
        return response.choices[0].message.content
    except Exception as e:
        return medicine_data.get("simple_explanation", "Please consult a doctor.")