from fastapi import FastAPI
from datetime import datetime
import random

# Create app instance with unique name
business_app = FastAPI(
    title="Connected Business API",
    description="Business Intelligence Platform",
    version="7.0.0"
)

@business_app.get("/")
async def root():
    return {
        "message": "🚀 BUSINESS API V7.0.0 - DEPLOYMENT SUCCESS!",
        "status": "operational", 
        "timestamp": datetime.now().isoformat(),
        "debug": "CLEAN_DEPLOYMENT_NO_CONFLICTS"
    }

@business_app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "Connected Business API",
        "version": "7.0.0",
        "timestamp": datetime.now().isoformat()
    }

@business_app.get("/dashboard")
async def dashboard():
    return {
        "revenue": 32480.75,
        "customers": 189,
        "transactions_today": random.randint(67, 124),
        "status": "LIVE",
        "deployment": "CLEAN_OVERRIDE_SUCCESS"
    }

@business_app.get("/customers")
async def customers():
    return {
        "total_customers": 189,
        "active_today": random.randint(45, 92),
        "satisfaction": 4.9
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(business_app, host="0.0.0.0", port=8000)
