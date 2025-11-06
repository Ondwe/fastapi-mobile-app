from fastapi import APIRouter, HTTPException, Depends, Request, Header, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

# Create the Auth Router
router = APIRouter(tags=["Authentication"])

# Pydantic models for request/response
class UserRegister(BaseModel):
    username: str
    email: str
    password: str
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    username: str
    premium: bool = False

# Simple in-memory user storage
users_db = {}

@router.post("/local/register", response_model=TokenResponse)
async def register(user_data: UserRegister):
    """Local registration endpoint"""
    # STRIP whitespace from username
    clean_username = user_data.username.strip()
    
    if clean_username in users_db:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Store user with clean username
    users_db[clean_username] = {
        "email": user_data.email.strip(),
        "password": user_data.password,
        "full_name": user_data.full_name.strip() if user_data.full_name else "",
        "premium": False
    }
    
    token = f"simple-token-{clean_username}"
    
    print(f"✅ Registered user: '{clean_username}'")
    print(f"   Users in DB: {list(users_db.keys())}")
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "username": clean_username,
        "premium": False
    }

@router.post("/local/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    """Local login endpoint"""
    # STRIP whitespace from username
    clean_username = credentials.username.strip()
    
    user = users_db.get(clean_username)
    if not user or user["password"] != credentials.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = f"simple-token-{clean_username}"
    
    print(f"✅ Logged in user: '{clean_username}'")
    
    return {
        "access_token": token,
        "token_type": "bearer", 
        "username": clean_username,
        "premium": user.get("premium", False)
    }

async def get_token_from_header(authorization: str = Header(None)):
    """Extract token from Authorization header"""
    if authorization and authorization.startswith("Bearer "):
        return authorization.replace("Bearer ", "")
    return None

async def get_token_from_query(token: str = Query(None)):
    """Extract token from query parameter"""
    return token

async def get_current_user(
    header_token: str = Depends(get_token_from_header),
    query_token: str = Depends(get_token_from_query)
):
    """Simplified token validation with username stripping"""
    print("🔄 Auth Check Started")
    print(f"   Header Token: {header_token}")
    print(f"   Query Token: {query_token}")
    
    # Get token from either source
    token = header_token or query_token
    
    if not token:
        print("❌ No token provided")
        raise HTTPException(status_code=401, detail="Authentication required")
    
    print(f"   Using Token: {token}")
    
    if token.startswith("simple-token-"):
        username = token.replace("simple-token-", "").strip()  # STRIP whitespace
        print(f"   Extracted Username: '{username}'")
        print(f"   Users in DB: {list(users_db.keys())}")
        
        # Check if user exists
        if username in users_db:
            print(f"✅ User found: '{username}'")
            return {
                "username": username, 
                "premium": users_db[username].get("premium", False)
            }
        else:
            print(f"❌ User not found in DB: '{username}'")
            # Let's try to find the user by stripping any extra spaces from DB keys
            for db_username in users_db.keys():
                if db_username.strip() == username:
                    print(f"✅ Found user after stripping: '{db_username}' -> '{username}'")
                    return {
                        "username": username,
                        "premium": users_db[db_username].get("premium", False)
                    }
    
    print(f"❌ Invalid token format: {token}")
    raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/users/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user

@router.get("/debug/token-check")
async def debug_token_check(
    header_token: str = Depends(get_token_from_header),
    query_token: str = Depends(get_token_from_query)
):
    """Debug endpoint to check token validation"""
    token = header_token or query_token
    
    result = {
        "token_received": token,
        "token_type": "header" if header_token else "query" if query_token else "none",
        "is_valid": token.startswith("simple-token-") if token else False,
        "users_in_db": list(users_db.keys()),
        "message": "Token check completed"
    }
    
    print(f"🔍 Token Check Result: {result}")
    return result

@router.post("/upgrade-premium/{username}")
async def upgrade_premium(username: str):
    """Upgrade user to premium"""
    clean_username = username.strip()  # STRIP whitespace
    
    if clean_username not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    users_db[clean_username]["premium"] = True
    
    print(f"⭐ Upgraded user to premium: '{clean_username}'")
    
    return {
        "message": f"User {clean_username} upgraded to premium",
        "username": clean_username,
        "premium": True
    }

@router.get("/user/analytics")
async def get_user_analytics(current_user: dict = Depends(get_current_user)):
    """Get user analytics and usage statistics"""
    return {
        "username": current_user["username"],
        "premium": current_user["premium"],
        "analytics": {
            "calculations_performed": 47,
            "text_operations": 23,
            "time_saved_hours": 12.5,
            "premium_features_used": 15 if current_user["premium"] else 0,
            "favorite_tool": "Advanced Calculator",
            "productivity_score": 88,
            "weekly_usage": [12, 19, 15, 25, 22, 18, 24]
        }
    }

@router.get("/user/activity")
async def get_user_activity(current_user: dict = Depends(get_current_user)):
    """Get user activity history"""
    return {
        "username": current_user["username"],
        "activities": [
            {
                "action": "Dashboard Accessed",
                "description": "Viewed personalized dashboard",
                "timestamp": "2 minutes ago",
                "icon": "fa-chart-line"
            },
            {
                "action": "Profile Updated", 
                "description": "Checked account information",
                "timestamp": "5 minutes ago",
                "icon": "fa-user-check"
            },
            {
                "action": "Calculation Performed",
                "description": "Used advanced calculator feature", 
                "timestamp": "1 hour ago",
                "icon": "fa-calculator"
            },
            {
                "action": "Text Tool Used",
                "description": "Processed text with formatting tools",
                "timestamp": "3 hours ago", 
                "icon": "fa-text-height"
            }
        ]
    }
