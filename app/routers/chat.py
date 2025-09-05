# app/routers/chat.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx
from app.config import settings

router = APIRouter(prefix="/chat", tags=["chat"])  # <-- NOT /api

class ChatIn(BaseModel):
    messages: list
    system: str | None = None
    temperature: float = 0.2
    model: str = "llama-3.3-70b-versatile"

@router.post("")  # "" => /chat
async def chat(body: ChatIn):
    payload = {
        "model": body.model,
        "messages": ([{"role": "system", "content": body.system}] if body.system else []) + body.messages,
        "temperature": body.temperature,
    }
    headers = {"Authorization": f"Bearer {settings.GROQ_API_KEY}", "Content-Type": "application/json"}
    url = "https://api.groq.com/openai/v1/chat/completions"
    try:
        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post(url, headers=headers, json=payload)
        r.raise_for_status()
        data = r.json()
        reply = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        return {"reply": reply}
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Groq error: {e}")
