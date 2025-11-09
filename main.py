from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import random
from datetime import datetime

app = FastAPI(
    title="Connected Business API",
    description="Business Intelligence Platform with AI Integration", 
    version="8.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# AI Agent Configuration
AI_AGENT_URL = "http://localhost:8080/api/ai/chat"
TIMEOUT = 30.0

@app.get("/")
async def root():
    return {
        "message": "🚀 Connected Business API v8.0.0 with AI Integration",
        "status": "operational", 
        "version": "8.0.0",
        "timestamp": datetime.now().isoformat(),
        "endpoints": ["/health", "/dashboard", "/customers", "/ai/chat", "/ai/health", "/integration/status"]
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "Connected Business API",
        "version": "8.0.0", 
        "timestamp": datetime.now().isoformat()
    }

@app.get("/dashboard")
async def dashboard():
    return {
        "revenue": 32480.75,
        "customers": 189,
        "transactions_today": random.randint(67, 124),
        "status": "LIVE",
        "deployment": "AI_INTEGRATED_v8"
    }

@app.get("/customers")
async def customers():
    return {
        "total_customers": 189,
        "active_today": random.randint(45, 92),
        "satisfaction": 4.9
    }

@app.post("/ai/chat")
async def ai_chat_proxy(message_data: dict):
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.post(
                AI_AGENT_URL,
                json=message_data,
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"AI Agent error: {response.text}"
                )
    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail="AI Agent unavailable - ensure it's running on localhost:8080"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"AI communication error: {str(e)}"
        )

@app.get("/ai/health")
async def ai_health_check():
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get("http://localhost:8080/health")
            return {
                "ai_agent_status": "online" if response.status_code == 200 else "offline",
                "timestamp": datetime.now().isoformat()
            }
    except:
        return {
            "ai_agent_status": "offline",
            "timestamp": datetime.now().isoformat(),
            "message": "AI Agent not reachable - ensure it's running on localhost:8080"
        }

@app.get("/integration/status")
async def integration_status():
    return {
        "business_api": "✅ Operational (v8.0.0)",
        "mobile_app_api": "✅ Running on Render",
        "ai_agent": "🔌 Requires local connection to localhost:8080", 
        "timestamp": datetime.now().isoformat(),
        "endpoints_available": [
            "/health", "/dashboard", "/customers",
            "/ai/chat", "/ai/health", "/integration/status"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
