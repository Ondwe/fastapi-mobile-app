from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import hashlib
import json
import os
from datetime import datetime

router = APIRouter()

# Simple file-based user storage
USERS_FILE = "local_users.json"

class UserRegister(BaseModel):
    username: str
    email: str
    password: str
    full_name: str = ""

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    username: str
    premium: bool

def simple_hash_password(password: str) -> str:
    """Simple password hashing (for demo only - use bcrypt in production)"""
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    """Load users from local JSON file"""
    try:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return {}

def save_users(users):
    """Save users to local JSON file"""
    try:
        with open(USERS_FILE, 'w') as f:
            json.dump(users, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving users: {e}")
        return False

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return simple_hash_password(plain_password) == hashed_password

@router.post("/register", response_model=Token)
async def register_user(user: UserRegister):
    try:
        users = load_users()
        print(f"Current users: {list(users.keys())}")
        
        # Check if username already exists
        if user.username in users:
            raise HTTPException(status_code=400, detail="Username already registered")
        
        # Create new user with simple hashing
        hashed_password = simple_hash_password(user.password)
        users[user.username] = {
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "hashed_password": hashed_password,
            "premium": False,
            "created_at": datetime.utcnow().isoformat()
        }
        
        if save_users(users):
            print(f"User {user.username} registered successfully")
            
            # Simple token (just the username for demo)
            access_token = f"simple-token-{user.username}"
            
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "username": user.username,
                "premium": False
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to save user")
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"Registration error: {e}")
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@router.post("/login", response_model=Token)
async def login_for_access_token(user: UserLogin):
    try:
        users = load_users()
        print(f"Available users: {list(users.keys())}")
        
        user_data = users.get(user.username)
        if not user_data:
            print(f"User {user.username} not found")
            raise HTTPException(status_code=401, detail="Incorrect username or password")
        
        if not verify_password(user.password, user_data["hashed_password"]):
            print(f"Invalid password for user {user.username}")
            raise HTTPException(status_code=401, detail="Incorrect username or password")
        
        print(f"User {user.username} logged in successfully")
        
        # Simple token (just the username for demo)
        access_token = f"simple-token-{user.username}"
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "username": user.username,
            "premium": user_data.get("premium", False)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Login error: {e}")
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")

@router.get("/users")
async def get_all_users():
    users = load_users()
    return {
        "total_users": len(users),
        "users": list(users.keys())
    }

@router.get("/status")
async def auth_status():
    return {
        "status": "online",
        "database": "local_file",
        "message": "Simple local authentication system working"
    }
