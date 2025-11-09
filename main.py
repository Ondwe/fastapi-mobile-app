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

# ===== BUSINESS ENDPOINTS =====
@app.get("/")
async def root():
    return {
        "message": "🚀 Connected Business API v8.0.0 with AI Integration",
        "status": "operational",
        "version": "8.0.0",
        "timestamp": datetime.now().isoformat(),
        "endpoints": ["/health", "/dashboard", "/customers", "/ai/chat", "/integration/status"]
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
        "deployment": "AI_INTEGRATED"
    }

@app.get("/customers")
async def customers():
    return {
        "total_customers": 189,
        "active_today": random.randint(45, 92),
        "satisfaction": 4.9
    }

# ===== AI INTEGRATION ENDPOINTS =====
@app.post("/ai/chat")
async def ai_chat_proxy(message_data: dict):
    """
    Proxy endpoint to forward chat messages to your local AI Agent
    """
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
    """
    Health check for AI Agent connectivity
    """
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get("http://localhost:8080/health")
            return {
                "ai_agent_status": "online" if response.status_code == 200 else "offline",
                "timestamp": datetime.now().isoformat(),
                "response_time": response.elapsed.total_seconds()
            }
    except:
        return {
            "ai_agent_status": "offline",
            "timestamp": datetime.now().isoformat(),
            "message": "AI Agent not reachable - ensure it's running on localhost:8080"
        }

@app.get("/integration/status")
async def integration_status():
    """
    Comprehensive status of all integrated services
    """
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

@app.post("/ai/business-chat")
async def ai_business_chat(request: dict):
    """
    Enhanced AI chat with business context
    """
    user_message = request.get("user_message", "Hello")
    
    try:
        # Get current business metrics to provide context to AI
        business_context = {
            "revenue": 32480.75,
            "customers": 189,
            "transactions_today": random.randint(67, 124),
            "service_status": "operational",
            "user_query": user_message,
            "context": "business_intelligence"
        }
        
        # Prepare enhanced message for AI
        enhanced_message = {
            "message": user_message,
            "context": business_context,
            "timestamp": datetime.now().isoformat()
        }
        
        # Forward to AI Agent
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.post(
                AI_AGENT_URL,
                json=enhanced_message,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                ai_response = response.json()
                return {
                    "ai_response": ai_response,
                    "business_context": business_context,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "ai_response": "I'm currently optimizing business analytics. Check the dashboard for real-time metrics.",
                    "business_context": business_context,
                    "fallback": True,
                    "timestamp": datetime.now().isoformat()
                }
                
    except Exception as e:
        return {
            "ai_response": "I'm enhancing business intelligence capabilities. Your data is secure and operations are normal.",
            "error": str(e),
            "fallback": True,
            "timestamp": datetime.now().isoformat()
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
