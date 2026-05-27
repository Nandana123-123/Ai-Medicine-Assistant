# remedies.py
# Ayurvedic and home remedies database

REMEDIES = {
    "fever": {
        "remedies": [
            "Drink tulsi (holy basil) tea 3 times a day",
            "Apply cold wet cloth on forehead",
            "Drink ginger and honey water",
            "Rest and drink plenty of fluids"
        ],
        "kannada": "ಜ್ವರಕ್ಕೆ ತುಳಸಿ ಚಹಾ ಕುಡಿಯಿರಿ"
    },
    "cold": {
        "remedies": [
            "Drink warm ginger tea with honey",
            "Steam inhalation with eucalyptus oil",
            "Drink turmeric milk at night",
            "Eat garlic with warm water"
        ],
        "kannada": "ಶೀತಕ್ಕೆ ಶುಂಠಿ ಚಹಾ ಕುಡಿಯಿರಿ"
    },
    "headache": {
        "remedies": [
            "Drink plenty of water",
            "Apply peppermint oil on temples",
            "Rest in quiet dark room",
            "Drink ginger tea"
        ],
        "kannada": "ತಲೆನೋವಿಗೆ ನೀರು ಕುಡಿಯಿರಿ"
    },
    "cough": {
        "remedies": [
            "Mix honey with ginger juice and take twice daily",
            "Gargle with warm salt water",
            "Drink turmeric milk",
            "Steam inhalation helps"
        ],
        "kannada": "ಕೆಮ್ಮಿಗೆ ಜೇನುತುಪ್ಪ ಮತ್ತು ಶುಂಠಿ ರಸ ತೆಗೆದುಕೊಳ್ಳಿ"
    },
    "stomach pain": {
        "remedies": [
            "Drink ajwain (carom seeds) water",
            "Drink warm water with lemon",
            "Eat light food like khichdi",
            "Drink jeera (cumin) water"
        ],
        "kannada": "ಹೊಟ್ಟೆ ನೋವಿಗೆ ಒಮ್ಮೆ ನೀರು ಕುಡಿಯಿರಿ"
    },
    "diabetes": {
        "remedies": [
            "Drink bitter gourd (karela) juice daily",
            "Eat fenugreek seeds soaked in water",
            "Avoid sugar and white rice",
            "Walk 30 minutes daily"
        ],
        "kannada": "ಮಧುಮೇಹಕ್ಕೆ ಹಾಗಲಕಾಯಿ ರಸ ಕುಡಿಯಿರಿ"
    },
    "acidity": {
        "remedies": [
            "Drink cold milk for instant relief",
            "Eat banana to reduce acidity",
            "Drink coconut water",
            "Avoid spicy and oily food"
        ],
        "kannada": "ಆಮ್ಲೀಯತೆಗೆ ತಣ್ಣನೆಯ ಹಾಲು ಕುಡಿಯಿರಿ"
    },
    "default": {
        "remedies": [
            "Drink plenty of water daily",
            "Eat fresh fruits and vegetables",
            "Get adequate sleep (7-8 hours)",
            "Consult a doctor for proper diagnosis"
        ],
        "kannada": "ಸಾಕಷ್ಟು ನೀರು ಕುಡಿಯಿರಿ ಮತ್ತು ವೈದ್ಯರನ್ನು ಸಂಪರ್ಕಿಸಿ"
    }
}


def get_remedies_for_medicine(medicine_name: str, uses: str) -> dict:
    """
    Find matching home remedies based on
    medicine name and its uses
    """
    medicine_lower = medicine_name.lower()
    uses_lower = uses.lower()
    combined = medicine_lower + " " + uses_lower

    # Check each illness keyword
    for illness, remedy_data in REMEDIES.items():
        if illness in combined:
            return {
                "illness": illness,
                "home_remedies": remedy_data["remedies"],
                "kannada_tip": remedy_data["kannada"]
            }

    # Return default if no match
    return {
        "illness": "general",
        "home_remedies": REMEDIES["default"]["remedies"],
        "kannada_tip": REMEDIES["default"]["kannada"]
    }