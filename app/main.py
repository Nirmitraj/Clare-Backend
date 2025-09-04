# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import chat as chat_router
from app.routers import contact

app = FastAPI(title="Clare Backend")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(chat_router.router)
app.include_router(contact.router, prefix="/api")

# Health endpoint for Render/Vercel checks
@app.get("/")
def health():
    return {"ok": True, "service": "clare-backend"}
