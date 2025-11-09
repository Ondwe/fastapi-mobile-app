"""
MAIN APPLICATION - Connected Business API
Definitive version for Render deployment
"""
from fastapi import FastAPI
from datetime import datetime
import random
import requests

app = FastAPI(
    title="Connected Business API",
    description="Business Intelligence Platform with AI Integration",
    version="5.0.0"
)

RENDER_URL = "https://fastapi-mobile-app.onrender.com"

class BusinessService:
    def __init__(self):
        self.render_available = self.check_render_connection()
    
    def check_render_connection(self):
        try:
            response = requests.get(f"{RENDER_URL}/health", timeout=5)
            return response.status_code == 200
        except:
            return False

service = BusinessService()

@app.get("/")
async def root():
    return {
        "message": "Connected Business API is running!",
        "version": "5.0.0",
        "status": "operational",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "Connected Business API",
        "version": "5.0.0",
        "render_connected": service.render_available,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/dashboard")
async def dashboard():
    data = {
        "total_revenue": 25480.50,
        "active_customers": 42,
        "pending_orders": random.randint(5, 15),
        "today_transactions": random.randint(10, 25),
        "conversion_rate": round(random.uniform(0.15, 0.25), 3),
        "business_status": "LIVE"
    }
    return {
        "dashboard": data,
        "quick_stats": {
            "daily_target": 1500.00,
            "target_progress": round((data["today_transactions"] * data["conversion_rate"]) / 1500 * 100, 1),
            "active_sessions": random.randint(15, 35)
        },
        "render_enhanced": service.render_available,
        "last_updated": datetime.now().isoformat()
    }

@app.get("/customers")
async def customers():
    return {
        "analytics": {
            "total_customers": 42,
            "new_customers_today": random.randint(1, 5),
            "repeat_customers": 28,
            "satisfaction_score": "⭐ 4.8/5.0",
            "top_categories": ["Electronics", "Services", "Consulting"]
        },
        "render_enhanced": service.render_available,
        "last_updated": datetime.now().isoformat()
    }

@app.get("/status")
async def status():
    return {
        "local_api": "healthy",
        "render_api": "connected" if service.render_available else "disconnected",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
