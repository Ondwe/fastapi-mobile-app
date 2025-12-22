from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
import os

app = FastAPI(title="HUMBU Mobile API", version="1.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files if directory exists
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return {"status": "HUMBU Mobile API is running", "contract": "$147,575/month"}

@app.get("/health")
async def health():
    return {"status": "healthy", "services": ["api", "dashboard", "ai"]}

@app.get("/dashboard")
async def dashboard():
    # Serve your main dashboard
    if os.path.exists("templates/dashboard.html"):
        return FileResponse("templates/dashboard.html")
    return {"message": "Dashboard coming soon"}

# Premium calculator endpoint
@app.get("/premium-calculator")
async def premium_calculator():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>HUMBU Premium Calculator</title>
        <style>
            body { font-family: Arial; padding: 20px; }
            .premium { background: gold; padding: 15px; border-radius: 10px; }
        </style>
    </head>
    <body>
        <h1>HUMBU Premium Calculator</h1>
        <div class="premium">
            <h3>💰 Contract Active: $147,575/month</h3>
            <p>This is the mobile/web extension of HUMBU Enterprise Platform</p>
        </div>
        <p><strong>Status:</strong> Connected to HUMBU Business Platform ✅</p>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
