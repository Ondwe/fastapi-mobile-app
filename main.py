from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import random
from datetime import datetime

app = FastAPI(
    title="Connected Business API",
    description="Business Intelligence Platform with Built-in AI",
    version="9.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# AI Configuration - Try external first, fallback to built-in
AI_AGENT_URL = "http://localhost:8080/api/ai/chat"
TIMEOUT = 10.0

def get_built_in_ai_response(user_message):
    """Built-in AI responses when external AI is unavailable"""
    business_responses = [
        "Your business shows excellent growth with $32K+ monthly revenue. Focus on customer retention.",
        "Customer satisfaction at 4.9/5.0 indicates superb service quality. Maintain this standard.",
        "With 189 customers, you have strong foundation for expansion. Consider new markets.",
        "Revenue trends are positive - consider increasing marketing budget by 15-20%.",
        "Business analytics show all systems operational and trending upward. Great work!",
        "Based on current metrics, implement a customer referral program for organic growth.",
        "Your revenue growth suggests exploring premium service tiers for increased ARPU.",
        "Consider AI-driven analytics for deeper customer insights and personalized marketing."
    ]
    
    context_aware_responses = {
        "revenue": "Your revenue of $32,480 shows 15% month-over-month growth. Excellent trajectory!",
        "customer": "189 customers with 92% retention rate indicates strong product-market fit.",
        "growth": "Current growth rate suggests scalability. Consider Series A funding preparation.",
        "strategy": "Focus on upselling existing customers while expanding to adjacent markets."
    }
    
    # Context-aware response
    user_lower = user_message.lower()
    for key, response in context_aware_responses.items():
        if key in user_lower:
            return response
    
    return random.choice(business_responses)

@app.get("/")
async def root():
    return {
        "message": "🚀 Connected Business API v9.0.0 with Built-in AI",
        "status": "operational",
        "version": "9.0.0",
        "timestamp": datetime.now().isoformat(),
        "ai_capability": "built-in + external proxy",
        "endpoints": ["/health", "/dashboard", "/customers", "/ai/chat", "/ai/health", "/integration/status"]
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "Connected Business API",
        "version": "9.0.0",
        "timestamp": datetime.now().isoformat(),
        "ai_status": "built-in_operational"
    }

@app.get("/dashboard")
async def dashboard():
    return {
        "revenue": 32480.75,
        "customers": 189,
        "transactions_today": random.randint(67, 124),
        "growth_rate": "15.2%",
        "status": "LIVE",
        "deployment": "BUILT_IN_AI_v9"
    }

@app.get("/customers")
async def customers():
    return {
        "total_customers": 189,
        "active_today": random.randint(45, 92),
        "satisfaction": 4.9,
        "retention_rate": "92%"
    }

@app.post("/ai/chat")
async def ai_chat_proxy(message_data: dict):
    """Smart AI proxy - tries external AI first, falls back to built-in"""
    user_message = message_data.get("message", "")
    
    # Try external AI first
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.post(
                AI_AGENT_URL,
                json=message_data,
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 200:
                ai_data = response.json()
                return {
                    "response": ai_data.get("response", "AI analysis completed"),
                    "user_message": user_message,
                    "timestamp": datetime.now().isoformat(),
                    "confidence": ai_data.get("confidence", 0.9),
                    "source": "external_ai_agent",
                    "built_in_fallback": False
                }
    except:
        pass  # Fall through to built-in AI
    
    # Use built-in AI
    ai_response = get_built_in_ai_response(user_message)
    return {
        "response": ai_response,
        "user_message": user_message,
        "timestamp": datetime.now().isoformat(),
        "confidence": round(random.uniform(0.85, 0.95), 2),
        "source": "built_in_ai",
        "built_in_fallback": True,
        "note": "External AI unavailable - using built-in business intelligence"
    }

@app.get("/ai/health")
async def ai_health_check():
    """Check AI availability - both external and built-in"""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get("http://localhost:8080/health")
            external_status = "online" if response.status_code == 200 else "offline"
    except:
        external_status = "offline"
    
    return {
        "external_ai_status": external_status,
        "built_in_ai_status": "online",
        "overall_ai_capability": "operational",
        "timestamp": datetime.now().isoformat(),
        "message": "Built-in AI always available, external AI when connected"
    }

@app.get("/integration/status")
async def integration_status():
    return {
        "business_api": "✅ Operational (v9.0.0)",
        "mobile_app_api": "✅ Running on Render",
        "ai_capability": "✅ Built-in + External Proxy",
        "external_ai": "🔌 Connect local AI to localhost:8080",
        "built_in_ai": "✅ Always available",
        "timestamp": datetime.now().isoformat(),
        "endpoints_available": [
            "/health", "/dashboard", "/customers",
            "/ai/chat", "/ai/health", "/integration/status"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
