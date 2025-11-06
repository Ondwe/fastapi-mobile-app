from fastapi import APIRouter, HTTPException, Depends
from app.auth import get_current_user

router = APIRouter(
    prefix="/premium",
    tags=["Premium"],
    responses={404: {"description": "Not found"}}
)

@router.get("/features")
async def premium_features_home(current_user: dict = Depends(get_current_user)):
    """Premium features overview."""
    if not current_user.get("premium", False):
        raise HTTPException(
            status_code=403, 
            detail={
                "error": "Premium feature required",
                "message": "Upgrade to premium to access exclusive features",
                "upgrade_url": "/premium/upgrade"
            }
        )
    
    return {
        "message": "Premium Features API", 
        "user": current_user["username"],
        "premium": current_user.get("premium", False),
        "features_available": [
            "Currency Converter",
            "Advanced Analytics", 
            "Priority Support",
            "Custom Themes",
            "Batch Processing"
        ]
    }

@router.get("/currency-convert/{amount}/{from_currency}/{to_currency}")
async def currency_convert(
    amount: float, 
    from_currency: str, 
    to_currency: str, 
    current_user: dict = Depends(get_current_user)
):
    """Mock currency conversion - premium feature"""
    if not current_user.get("premium", False):
        raise HTTPException(
            status_code=403, 
            detail={
                "error": "Premium feature required",
                "message": "Upgrade to premium to access currency conversion",
                "upgrade_url": "/premium/upgrade"
            }
        )
    
    # Mock conversion rates
    rates = {
        "USD": {"EUR": 0.85, "GBP": 0.73, "JPY": 110.0, "CAD": 1.25},
        "EUR": {"USD": 1.18, "GBP": 0.86, "JPY": 129.0, "CAD": 1.47},
        "GBP": {"USD": 1.37, "EUR": 1.16, "JPY": 150.0, "CAD": 1.71},
        "JPY": {"USD": 0.0091, "EUR": 0.0078, "GBP": 0.0067, "CAD": 0.011},
        "CAD": {"USD": 0.80, "EUR": 0.68, "GBP": 0.58, "JPY": 90.0}
    }
    
    if from_currency not in rates or to_currency not in rates[from_currency]:
        raise HTTPException(status_code=400, detail="Unsupported currency pair")
    
    rate = rates[from_currency][to_currency]
    converted_amount = amount * rate
    
    return {
        "original_amount": amount,
        "from_currency": from_currency,
        "to_currency": to_currency,
        "converted_amount": round(converted_amount, 2),
        "exchange_rate": rate,
        "user": current_user["username"],
        "timestamp": "2024-01-01T00:00:00Z"  # Mock timestamp
    }

@router.get("/analytics")
async def get_premium_analytics(current_user: dict = Depends(get_current_user)):
    """Premium analytics dashboard."""
    if not current_user.get("premium", False):
        raise HTTPException(
            status_code=403, 
            detail="Premium feature required. Upgrade to access advanced analytics."
        )
    
    return {
        "message": f"Premium analytics for user: {current_user['username']}",
        "analytics": {
            "usage_trends": [65, 78, 92, 81, 56, 55, 40],
            "top_features": ["Calculator", "Text Tools", "Currency Converter"],
            "time_saved": "15.2 hours",
            "productivity_score": 87,
            "recommendations": [
                "Try batch processing for multiple calculations",
                "Use currency converter for international transactions",
                "Explore advanced text analysis tools"
            ]
        },
        "user": current_user["username"],
        "premium_since": "2024-01-01"
    }

@router.get("/user/stats")
async def get_user_stats(current_user: dict = Depends(get_current_user)):
    """Get user statistics and activity."""
    return {
        "username": current_user["username"],
        "premium": current_user.get("premium", False),
        "stats": {
            "calculations_performed": 47,
            "text_operations": 23,
            "premium_features_used": 15 if current_user.get("premium", False) else 0,
            "member_since": "2024-01-15",
            "total_time_saved": "12.5 hours"
        },
        "recent_activity": [
            {"action": "Currency Conversion", "timestamp": "2024-01-20 10:30:00", "details": "100 USD to EUR"},
            {"action": "Text Analysis", "timestamp": "2024-01-20 09:15:00", "details": "Word count analysis"},
            {"action": "Advanced Calculation", "timestamp": "2024-01-19 16:45:00", "details": "Power calculation"}
        ]
    }
