import os
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv

load_dotenv()

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

JWT_SECRET = os.getenv("JWT_SECRET", "my_super_secret_key_change_123")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_HOURS = 24


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_id: str, email: str) -> str:
    expire = datetime.utcnow() + timedelta(hours=JWT_EXPIRE_HOURS)
    payload = {
        "sub": str(user_id),
        "email": email,
        "exp": expire
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    print(f"Token created for: {email}")
    return token


def decode_token(token: str) -> dict:
    try:
        # Clean token - remove Bearer if accidentally included
        token = token.replace("Bearer ", "").strip()
        
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM]
        )
        print(f"Token decoded successfully for: {payload.get('email')}")
        return payload
    except JWTError as e:
        print(f"JWT Error: {str(e)}")
        return None
    except Exception as e:
        print(f"Token decode error: {str(e)}")
        return None