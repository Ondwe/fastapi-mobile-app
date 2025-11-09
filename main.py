from fastapi import FastAPI
from datetime import datetime
import random

# Create app instance - MUST be named 'app' for uvicorn
app = FastAPI(
    title="Connected Business API",
    description="Business Intelligence Platform",
    version="7.0.0"
)

@app.get("/")
async def root():
    return {
        "message": "🚀 BUSINESS API V7.0.0 - FINAL DEPLOYMENT SUCCESS!",
        "status": "operational",
        "timestamp": datetime.now().isoformat(),
        "debug": "FIXED_APP_REFERENCE"
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "Connected Business API",
        "version": "7.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/dashboard")
async def dashboard():
    return {
        "revenue": 32480.75,
        "customers": 189,
        "transactions_today": random.randint(67, 124),
        "status": "LIVE",
        "deployment": "FINAL_SUCCESS"
    }

@app.get("/customers")
async def customers():
    return {
        "total_customers": 189,
        "active_today": random.randint(45, 92),
        "satisfaction": 4.9
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
