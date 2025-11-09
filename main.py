from fastapi import FastAPI
from datetime import datetime
import random
import requests

app = FastAPI(
    title="Connected Business API",
    description="Business Intelligence Platform",
    version="7.0.0"
)

@app.get("/")
async def root():
    return {
        "message": "Connected Business API is running!",
        "version": "7.0.0",
        "status": "operational",
        "timestamp": datetime.now().isoformat()
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
        "revenue": 25480.50,
        "customers": 42,
        "transactions_today": random.randint(10, 25),
        "pending_orders": random.randint(5, 15),
        "status": "LIVE",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/customers")
async def customers():
    return {
        "total_customers": 42,
        "satisfaction": "⭐ 4.8/5.0",
        "new_today": random.randint(1, 5),
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
