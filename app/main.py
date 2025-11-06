from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.auth import router as auth_router, get_current_user
from app.routers import text_tools, calculator, premium

# Create FastAPI app
app = FastAPI(
    title="FastAPI Mobile App API",
    description="A comprehensive mobile app with calculator, text tools, and premium features",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api")
app.include_router(text_tools.router)
app.include_router(calculator.router)
app.include_router(premium.router, prefix="/api")

# Basic routes
@app.get("/")
async def home_page(request: Request):
    """Returns the main home page template."""
    return templates.TemplateResponse("home_secure.html", {"request": request})

@app.get("/dashboard")
async def dashboard_page(request: Request, current_user: dict = Depends(get_current_user)):
    """Dashboard page - requires authentication"""
    return templates.TemplateResponse("dashboard.html", {
        "request": request, 
        "user": current_user
    })

@app.get("/health")
async def health_check():
    """Simple health check endpoint."""
    return {
        "status": "healthy", 
        "message": "FastAPI Mobile App API is running",
        "version": "2.0.0",
        "features": ["authentication", "calculator", "text_tools", "premium_features"]
    }

@app.get("/test-auth")
async def test_auth_page(request: Request):
    """Returns the test authentication page template."""
    return templates.TemplateResponse("test_auth.html", {"request": request})

@app.get("/api/status")
async def api_status(current_user: dict = Depends(get_current_user)):
    """API status with user information."""
    return {
        "status": "operational",
        "user": current_user["username"],
        "premium": current_user["premium"],
        "features_available": [
            "text_tools",
            "calculator", 
            "premium_features" if current_user["premium"] else "basic_features"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
