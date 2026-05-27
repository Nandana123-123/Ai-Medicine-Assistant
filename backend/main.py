# main.py
# This is the entry point of our FastAPI application

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

# Import all route files
from routes.auth import router as auth_router

# Create FastAPI app
app = FastAPI(
    title="AI Medicine Assistant",
    description="AI-Based Medicine Identification and Healthcare Assistant",
    version="1.0.0"
)

# ─── CORS MIDDLEWARE ──────────────────────────────────
# Allows frontend to talk to backend

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your Vercel URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── INCLUDE ROUTES ───────────────────────────────────

app.include_router(auth_router, tags=["Authentication"])

# More routes will be added in Day 3:
# app.include_router(medicine_router, tags=["Medicine"])
# app.include_router(chatbot_router, tags=["Chatbot"])


# ─── ROOT ENDPOINT ────────────────────────────────────

@app.get("/")
async def root():
    return {
        "message": "🏥 AI Medicine Assistant API is running!",
        "version": "1.0.0",
        "status": "healthy"
    }


@app.get("/health")
async def health_check():
    return {"status": "OK"}


# ─── RUN SERVER ───────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Auto-restart when code changes
    )