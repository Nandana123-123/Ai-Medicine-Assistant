from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.auth import router as auth_router
from routes.medicine import router as medicine_router
from routes.chatbot import router as chatbot_router
from routes.profile import router as profile_router

app = FastAPI(title="AI Medicine Assistant", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, tags=["Auth"])
app.include_router(medicine_router, tags=["Medicine"])
app.include_router(chatbot_router, tags=["Chatbot"])
app.include_router(profile_router, prefix="/user", tags=["Profile"])

@app.get("/")
async def root():
    return {"message": "AI Medicine Assistant Running!", "status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)