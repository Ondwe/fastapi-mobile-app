from fastapi import FastAPI, HTTPException
from datetime import datetime, timedelta
import random
import requests
import asyncio

app = FastAPI(
    title="Connected Business API",
    description="Unified API connecting local features with Render AI",
    version="3.0.0"
)

# Configuration
RENDER_URL = "https://fastapi-mobile-app.onrender.com"

class BusinessService:
    def __init__(self):
        self.render_available = False
        self.check_render_connection()
    
    def check_render_connection(self):
        """Check if Render API is available"""
        try:
            response = requests.get(f"{RENDER_URL}/health", timeout=5)
            self.render_available = response.status_code == 200
            print(f"🌐 Render API: {'✅ AVAILABLE' if self.render_available else '❌ UNAVAILABLE'}")
        except:
            self.render_available = False
    
    def generate_business_data(self):
        """Generate realistic business data"""
        return {
            "total_revenue": 25480.50,
            "active_customers": 42,
            "pending_orders": random.randint(5, 15),
            "today_transactions": random.randint(10, 25),
            "conversion_rate": round(random.uniform(0.15, 0.25), 3),
            "business_status": "LIVE"
        }
    
    def generate_customer_insights(self):
        """Generate customer analytics"""
        return {
            "total_customers": 42,
            "new_customers_today": random.randint(1, 5),
            "repeat_customers": 28,
            "satisfaction_score": "⭐ 4.8/5.0",
            "top_categories": ["Electronics", "Services", "Consulting"],
            "retention_rate": "87%"
        }

service = BusinessService()

@app.get("/")
async def root():
    return {
        "service": "Connected Business API",
        "version": "3.0.0",
        "status": "operational",
        "render_connected": service.render_available,
        "endpoints": {
            "dashboard": "/dashboard - Business overview",
            "customers": "/customers - Customer analytics",
            "transactions": "/transactions - Recent activity",
            "revenue": "/revenue - Financial data",
            "products": "/products - Product catalog",
            "health": "/health - System status"
        }
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "Connected Business API",
        "render_connected": service.render_available,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/dashboard")
async def mobile_dashboard():
    """Mobile business dashboard"""
    data = service.generate_business_data()
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
async def customer_analytics():
    """Customer insights for mobile"""
    insights = service.generate_customer_insights()
    
    # Add AI enhancements if Render is available
    if service.render_available:
        insights["ai_predictions"] = {
            "churn_risk": f"{random.randint(5, 15)}%",
            "growth_forecast": f"+{random.randint(10, 25)}% next month",
            "recommendations": ["Focus on retention", "Upsell premium services"]
        }
    
    return {
        "analytics": insights,
        "render_enhanced": service.render_available,
        "last_updated": datetime.now().isoformat()
    }

@app.get("/transactions")
async def recent_transactions(limit: int = 10):
    """Recent transactions for mobile"""
    transactions = []
    for i in range(limit):
        transactions.append({
            "id": f"TXN{1000 + i}",
            "amount": round(random.uniform(50, 500), 2),
            "customer": f"Customer {i+1}",
            "type": random.choice(["sale", "service", "consultation"]),
            "status": random.choice(["completed", "pending"]),
            "timestamp": (datetime.now() - timedelta(hours=random.randint(1, 24))).isoformat()
        })
    
    return {
        "transactions": sorted(transactions, key=lambda x: x["timestamp"], reverse=True),
        "summary": {
            "total_count": len(transactions),
            "total_amount": sum(t["amount"] for t in transactions),
            "average_amount": sum(t["amount"] for t in transactions) / len(transactions) if transactions else 0
        },
        "render_enhanced": service.render_available
    }

@app.get("/revenue")
async def revenue_data(days: int = 7):
    """Revenue data for mobile dashboard"""
    revenue_days = []
    total_revenue = 0
    
    for i in range(days):
        day_revenue = round(random.uniform(800, 2500), 2)
        revenue_days.append({
            "date": (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d"),
            "revenue": day_revenue,
            "transactions": random.randint(8, 22)
        })
        total_revenue += day_revenue
    
    return {
        "period_days": days,
        "revenue_data": revenue_days,
        "total_revenue": total_revenue,
        "daily_average": round(total_revenue / days, 2),
        "growth": f"+{random.randint(5, 15)}%",
        "render_enhanced": service.render_available
    }

@app.get("/products")
async def popular_products():
    """Popular products for mobile app"""
    products = [
        {"id": 1, "name": "Premium Widget", "price": 199.99, "sales": random.randint(50, 200), "category": "Electronics"},
        {"id": 2, "name": "Business Consultation", "price": 299.99, "sales": random.randint(30, 100), "category": "Services"},
        {"id": 3, "name": "Standard Package", "price": 99.99, "sales": random.randint(100, 300), "category": "Services"},
        {"id": 4, "name": "Mobile App Service", "price": 149.99, "sales": random.randint(40, 120), "category": "Digital"},
        {"id": 5, "name": "Support Plan", "price": 79.99, "sales": random.randint(80, 180), "category": "Services"}
    ]
    
    return {
        "popular_products": sorted(products, key=lambda x: x["sales"], reverse=True),
        "total_products": len(products),
        "top_category": max([p["category"] for p in products], key=[p["category"] for p in products].count),
        "render_enhanced": service.render_available
    }

@app.get("/status")
async def connection_status():
    """Check connection status with Render"""
    render_status = "unknown"
    try:
        response = requests.get(f"{RENDER_URL}/health", timeout=10)
        if response.status_code == 200:
            render_data = response.json()
            render_status = f"connected (v{render_data.get('version', 'unknown')})"
        else:
            render_status = "error"
    except:
        render_status = "disconnected"
    
    return {
        "local_api": "healthy",
        "render_api": render_status,
        "connected_system": "operational",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
