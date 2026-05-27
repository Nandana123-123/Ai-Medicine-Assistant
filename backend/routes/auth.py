# auth.py
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from database import get_db
from utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_token
)

router = APIRouter()
security = HTTPBearer()


class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    preferred_language: str = "english"


class LoginRequest(BaseModel):
    email: str
    password: str


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token. Please login again."
        )
    return payload


@router.post("/register")
async def register(data: RegisterRequest):
    db = get_db()

    try:
        # Check if email exists
        existing = db.table("users")\
            .select("id")\
            .eq("email", data.email)\
            .execute()

        if len(existing.data) > 0:
            raise HTTPException(
                status_code=400,
                detail="Email already registered. Please login."
            )

        # Hash password
        hashed = hash_password(data.password)

        # Insert user
        result = db.table("users").insert({
            "name": data.name,
            "email": data.email,
            "password_hash": hashed,
            "preferred_language": data.preferred_language
        }).execute()

        print("Insert result:", result)  # Debug log

        if not result.data:
            raise HTTPException(
                status_code=500,
                detail="Failed to create user. Check Supabase table."
            )

        new_user = result.data[0]

        token = create_access_token(
            user_id=str(new_user["id"]),
            email=new_user["email"]
        )

        return {
            "message": "Registration successful!",
            "token": token,
            "user": {
                "id": new_user["id"],
                "name": new_user["name"],
                "email": new_user["email"],
                "preferred_language": new_user["preferred_language"]
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"Register error: {str(e)}")  # Debug log
        raise HTTPException(
            status_code=500,
            detail=f"Registration failed: {str(e)}"
        )


@router.post("/login")
async def login(data: LoginRequest):
    db = get_db()

    try:
        result = db.table("users")\
            .select("*")\
            .eq("email", data.email)\
            .execute()

        if not result.data or len(result.data) == 0:
            raise HTTPException(
                status_code=401,
                detail="Email not found. Please register first."
            )

        user = result.data[0]

        if not verify_password(data.password, user["password_hash"]):
            raise HTTPException(
                status_code=401,
                detail="Wrong password. Please try again."
            )

        token = create_access_token(
            user_id=str(user["id"]),
            email=user["email"]
        )

        return {
            "message": "Login successful!",
            "token": token,
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "preferred_language": user["preferred_language"]
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"Login error: {str(e)}")  # Debug log
        raise HTTPException(
            status_code=500,
            detail=f"Login failed: {str(e)}"
        )


@router.get("/profile")
async def get_profile(current_user: dict = Depends(get_current_user)):
    db = get_db()
    try:
        result = db.table("users")\
            .select("id, name, email, preferred_language, created_at")\
            .eq("id", current_user["sub"])\
            .execute()

        if not result.data:
            raise HTTPException(status_code=404, detail="User not found")

        return {"user": result.data[0]}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/logout")
async def logout(current_user: dict = Depends(get_current_user)):
    return {"message": "Logged out successfully!"}