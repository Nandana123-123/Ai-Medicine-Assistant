# chatbot.py
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from groq import Groq
from database import get_db
from utils.security import decode_token
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()
security = HTTPBearer()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


class ChatRequest(BaseModel):
    message: str
    medicine_name: str = ""


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Please login first")
    return payload


@router.post("/chatbot")
async def chat(
    data: ChatRequest,
    current_user: dict = Depends(get_current_user)
):
    db = get_db()
    try:
        system_prompt = """You are a helpful healthcare assistant for 
        uneducated users in India. Use simple language. Always recommend 
        consulting a doctor for serious issues."""

        context = ""
        if data.medicine_name:
            context = f"User is asking about: {data.medicine_name}. "

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": context + data.message}
            ],
            max_tokens=500
        )

        answer = response.choices[0].message.content

        try:
            db.table("chatbot_history").insert({
                "user_id": current_user["sub"],
                "question": data.message,
                "answer": answer
            }).execute()
        except Exception as db_err:
            print(f"DB error: {db_err}")

        return {
            "question": data.message,
            "answer": answer,
            "disclaimer": "Please consult a doctor for medical advice."
        }

    except Exception as e:
        print(f"Chatbot error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/chatbot/history")
async def get_chat_history(
    current_user: dict = Depends(get_current_user)
):
    db = get_db()
    try:
        result = db.table("chatbot_history")\
            .select("*")\
            .eq("user_id", current_user["sub"])\
            .order("created_at", desc=True)\
            .limit(20)\
            .execute()
        return {"history": result.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))