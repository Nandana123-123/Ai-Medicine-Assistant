# medicine.py
# Handles medicine image upload and AI identification

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from database import get_db
from utils.security import decode_token
from services.ocr_service import extract_text_from_image
from services.ai_service import identify_medicine, simplify_for_uneducated_user
from services.translate_service import translate_medicine_data
from utils.remedies import get_remedies_for_medicine

router = APIRouter()
security = HTTPBearer()

# Allowed image types
ALLOWED_TYPES = ["image/jpeg", "image/png", "image/jpg", "image/webp"]


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Please login first"
        )
    return payload


@router.post("/upload-image")
async def upload_medicine_image(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """
    Main endpoint - user uploads medicine image
    Returns complete medicine information
    """
    db = get_db()

    # Validate file type
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Please upload a valid image (JPG, PNG, WEBP)"
        )

    # Validate file size (max 10MB)
    image_bytes = await file.read()
    if len(image_bytes) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="Image too large. Please upload image under 10MB"
        )

    try:
        print("Step 1: Extracting text from image...")
        ocr_text = extract_text_from_image(image_bytes)

        if not ocr_text:
            raise HTTPException(
                status_code=400,
                detail="Could not read text from image. Please upload a clearer image."
            )

        print("Step 2: Identifying medicine with AI...")
        medicine_data = identify_medicine(ocr_text)

        print("Step 3: Simplifying explanation...")
        simple_explanation = simplify_for_uneducated_user(medicine_data)
        medicine_data["simple_explanation"] = simple_explanation

        print("Step 4: Translating to Kannada...")
        kannada_data = translate_medicine_data(medicine_data)

        print("Step 5: Getting home remedies...")
        remedies = get_remedies_for_medicine(
            medicine_data.get("medicine_name", ""),
            medicine_data.get("uses", "")
        )

        print("Step 6: Saving to database...")
        try:
            db.table("user_history").insert({
                "user_id": current_user["sub"],
                "medicine_name": medicine_data.get("medicine_name"),
                "result_english": str(medicine_data),
                "result_kannada": str(kannada_data)
            }).execute()
        except Exception as db_error:
            print(f"DB save error (non-critical): {db_error}")

        return {
            "success": True,
            "ocr_text": ocr_text,
            "medicine_english": medicine_data,
            "medicine_kannada": kannada_data,
            "home_remedies": remedies,
            "disclaimer": "This is for educational purposes only. Please consult a doctor before taking any medicine."
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"Upload error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing image: {str(e)}"
        )


@router.get("/history")
async def get_history(current_user: dict = Depends(get_current_user)):
    """Get user's medicine upload history"""
    db = get_db()

    try:
        result = db.table("user_history")\
            .select("*")\
            .eq("user_id", current_user["sub"])\
            .order("uploaded_at", desc=True)\
            .limit(20)\
            .execute()

        return {
            "history": result.data,
            "total": len(result.data)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))