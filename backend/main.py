# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.auth import router as auth_router
from routes.medicine import router as medicine_router

app = FastAPI(
    title="AI Medicine Assistant",
    description="AI-Based Medicine Identification",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(auth_router, tags=["Authentication"])
app.include_router(medicine_router, tags=["Medicine"])


@app.get("/")
async def root():
    return {
        "message": "AI Medicine Assistant API Running!",
        "status": "healthy"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)