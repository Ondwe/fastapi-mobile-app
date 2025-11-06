from fastapi import APIRouter, HTTPException, Depends, Header
from app.auth import get_current_user

router = APIRouter(tags=["Premium"])

async def get_token_from_header(authorization: str = Header(None)):
    """Extract token from Authorization header"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")
    
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization format")
    
    return authorization.replace("Bearer ", "")

@router.get("/premium-features")
async def premium_features_home(current_user: dict = Depends(get_current_user)):
    return {
        "message": "Premium Features API", 
        "user": current_user["username"],
        "premium": current_user.get("premium", False),
        "features_available": ["Currency Converter", "Advanced Analytics", "Priority Support"]
    }

@router.get("/currency-convert/{amount}/{from_currency}/{to_currency}")
async def currency_convert(
    amount: float, 
    from_currency: str, 
    to_currency: str, 
    token: str = Depends(get_token_from_header),
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
        "USD": {"EUR": 0.85, "GBP": 0.73, "JPY": 110.0},
        "EUR": {"USD": 1.18, "GBP": 0.86, "JPY": 129.0},
        "GBP": {"USD": 1.37, "EUR": 1.16, "JPY": 150.0},
        "JPY": {"USD": 0.0091, "EUR": 0.0078, "GBP": 0.0067}
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
        "user": current_user["username"]
    }

@router.get("/premium/data")
async def get_premium_data(current_user: dict = Depends(get_current_user)):
    if not current_user.get("premium", False):
        raise HTTPException(
            status_code=403, 
            detail="Premium feature required. Upgrade to access exclusive data."
        )
    
    return {
        "message": f"Premium data for user: {current_user['username']}",
        "exclusive_data": ["Advanced Analytics", "Priority Support", "Custom Themes", "API Access"],
        "user": current_user["username"],
        "premium_since": "2024-01-01"  # Mock date
    }

@router.get("/user/stats")
async def get_user_stats(current_user: dict = Depends(get_current_user)):
    """Get user statistics and activity"""
    return {
        "username": current_user["username"],
        "premium": current_user.get("premium", False),
        "stats": {
            "calculations_performed": 12,
            "text_operations": 8,
            "premium_features_used": 3,
            "member_since": "2024-01-15"
        },
        "recent_activity": [
            {"action": "Currency Conversion", "timestamp": "2024-01-20 10:30:00"},
            {"action": "Text Reversal", "timestamp": "2024-01-20 09:15:00"},
            {"action": "Advanced Calculation", "timestamp": "2024-01-19 16:45:00"}
        ]
    }
