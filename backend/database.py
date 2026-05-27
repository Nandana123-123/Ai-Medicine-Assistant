import os
from pathlib import Path
from supabase import create_client, Client
from dotenv import load_dotenv

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

print(f"URL found: {bool(SUPABASE_URL)}")
print(f"KEY found: {bool(SUPABASE_KEY)}")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise Exception("❌ Supabase URL or KEY missing in .env file!")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
print("✅ Database connected successfully!")

def get_db():
    return supabase