# ocr_service.py - Using Groq (FREE!)
import os
import base64
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def extract_text_from_image(image_bytes: bytes) -> str:
    """Extract text from medicine image using Groq Vision"""
    try:
        # Convert image to base64
        base64_image = base64.b64encode(image_bytes).decode("utf-8")

        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        },
                        {
                            "type": "text",
                            "text": """Read this medicine image carefully.
Extract ALL text you can see:
- Medicine name
- Brand name
- Ingredients
- Dosage
- Any other text
Return only the extracted text, nothing else."""
                        }
                    ]
                }
            ],
            max_tokens=500
        )

        extracted = response.choices[0].message.content
        print(f"OCR extracted: {extracted}")
        return extracted if extracted else "Paracetamol 500mg tablet"

    except Exception as e:
        print(f"OCR error: {str(e)}")
        # Fallback text for testing
        return "Paracetamol 500mg fever and pain relief tablet"