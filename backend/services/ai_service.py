# ai_service.py - Using Groq (FREE!)
import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"


def get_default_medicine_response() -> dict:
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
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a medical assistant. Reply with valid JSON only. No extra text."
                },
                {
                    "role": "user",
                    "content": f"""Based on this medicine text: "{ocr_text}"

Return ONLY this JSON, nothing else:
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
    "simple_explanation": "simple explanation for uneducated users"
}}"""
                }
            ],
            max_tokens=1000
        )

        result = response.choices[0].message.content.strip()

        # Clean markdown if present
        if "```" in result:
            result = result.split("```")[1]
            if result.startswith("json"):
                result = result[4:]

        return json.loads(result.strip())

    except json.JSONDecodeError:
        print("JSON parse error - returning default")
        return get_default_medicine_response()
    except Exception as e:
        print(f"AI error: {str(e)}")
        return get_default_medicine_response()


def simplify_for_uneducated_user(medicine_data: dict) -> str:
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": f"""Explain in very simple words for uneducated rural users. 
Maximum 3 short sentences. No medical jargon.
Medicine: {medicine_data.get('medicine_name')}
Uses: {medicine_data.get('uses')}
Side effects: {medicine_data.get('side_effects')}"""
                }
            ],
            max_tokens=150
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Simplify error: {str(e)}")
        return medicine_data.get("simple_explanation", "Please consult a doctor.")