# translate_service.py
# Translates medicine info to Kannada

from deep_translator import GoogleTranslator


def translate_to_kannada(text: str) -> str:
    """Translate English text to Kannada"""
    try:
        if not text or len(text.strip()) == 0:
            return text

        translator = GoogleTranslator(
            source='english',
            target='kannada'
        )

        # Split long text into chunks (max 4000 chars)
        if len(text) > 4000:
            text = text[:4000]

        translated = translator.translate(text)
        return translated

    except Exception as e:
        print(f"Translation error: {str(e)}")
        return text  # Return original if translation fails


def translate_medicine_data(medicine_data: dict) -> dict:
    """Translate all medicine fields to Kannada"""
    try:
        kannada_data = {}

        fields_to_translate = [
            "uses", "advantages", "side_effects",
            "warnings", "simple_explanation",
            "when_to_see_doctor"
        ]

        for key, value in medicine_data.items():
            if key in fields_to_translate and value:
                kannada_data[key] = translate_to_kannada(str(value))
            else:
                kannada_data[key] = value

        return kannada_data

    except Exception as e:
        print(f"Medicine translation error: {str(e)}")
        return medicine_data