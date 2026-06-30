from fastapi import FastAPI

from app.service.api import router as chat_router
from app.utils.config import Settings

app = FastAPI(title=settings.app_name)
#Mount the chart router
app.include_router(chat_router)

@app.get("/")
async def root():
    return {
        "app": settings.app_name,
        "version": settings.app_env,
        "message":"Package tracking assistant is returning.",
        
    }