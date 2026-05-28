# translate_service.py
from deep_translator import GoogleTranslator


def translate_to_kannada(text: str) -> str:
    """Translate English text to Kannada"""
    try:
        if not text or len(text.strip()) == 0:
            return text

        # Split into chunks of 500 chars for better translation
        if len(text) <= 500:
            translator = GoogleTranslator(source='auto', target='kn')
            result = translator.translate(text)
            return result if result else text

        # For longer text, translate in chunks
        chunks = [text[i:i+500] for i in range(0, len(text), 500)]
        translated_chunks = []

        for chunk in chunks:
            translator = GoogleTranslator(source='auto', target='kn')
            translated = translator.translate(chunk)
            translated_chunks.append(translated if translated else chunk)

        return ' '.join(translated_chunks)

    except Exception as e:
        print(f"Translation error: {str(e)}")
        return text


def translate_medicine_data(medicine_data: dict) -> dict:
    """Translate all medicine fields to Kannada"""
    try:
        kannada_data = {}

        # These fields get translated
        fields_to_translate = [
            "uses", "advantages", "side_effects",
            "warnings", "simple_explanation",
            "when_to_see_doctor", "dosage",
            "storage", "category"
        ]

        for key, value in medicine_data.items():
            if key in fields_to_translate and value:
                print(f"Translating {key}...")
                kannada_data[key] = translate_to_kannada(str(value))
            else:
                # Keep original for name fields
                kannada_data[key] = value

        return kannada_data

    except Exception as e:
        print(f"Medicine translation error: {str(e)}")
        return medicine_data