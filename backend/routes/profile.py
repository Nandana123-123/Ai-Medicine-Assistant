# profile.py
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from database import get_db
from utils.security import decode_token

router = APIRouter()
security = HTTPBearer()


class UpdateProfile(BaseModel):
    name: str = ""
    preferred_language: str = "english"


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Please login first")
    return payload


@router.get("/profile")
async def get_profile(current_user: dict = Depends(get_current_user)):
    db = get_db()
    try:
        user_id = current_user["sub"]
        print(f"Getting profile for user_id: {user_id}")

        # Get user info
        user = db.table("users")\
            .select("id, name, email, preferred_language, created_at")\
            .eq("id", user_id)\
            .execute()

        if not user.data:
            raise HTTPException(status_code=404, detail="User not found")

        # Get medicine history count
        history = db.table("user_history")\
            .select("id")\
            .eq("user_id", user_id)\
            .execute()

        print(f"History count: {len(history.data)}")

        # Get chatbot history count
        chats = db.table("chatbot_history")\
            .select("id")\
            .eq("user_id", user_id)\
            .execute()

        print(f"Chat count: {len(chats.data)}")

        return {
            "user": user.data[0],
            "stats": {
                "medicines_scanned": len(history.data),
                "chat_messages": len(chats.data)
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Profile error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/profile/update")
async def update_profile(
    data: UpdateProfile,
    current_user: dict = Depends(get_current_user)
):
    db = get_db()
    try:
        update_data = {}
        if data.name:
            update_data["name"] = data.name
        if data.preferred_language:
            update_data["preferred_language"] = data.preferred_language

        result = db.table("users")\
            .update(update_data)\
            .eq("id", current_user["sub"])\
            .execute()

        return {"message": "Profile updated!", "user": result.data[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))