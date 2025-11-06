from fastapi import APIRouter, HTTPException
import requests

router = APIRouter()

AI_AGENT_URL = "http://localhost:8080"

@router.post("/ai-chat")
async def ai_chat(message: str):
    """Send message to AI agent and get response"""
    try:
        response = requests.post(
            f"{AI_AGENT_URL}/chat",
            json={"message": message},
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=500, detail="AI agent unavailable")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")

@router.get("/ai-status")
async def ai_status():
    """Check if AI agent is available"""
    try:
        response = requests.get(f"{AI_AGENT_URL}/", timeout=5)
        return {"status": "online", "service": "Gemini AI Agent"}
    except:
        return {"status": "offline", "service": "Gemini AI Agent"}
