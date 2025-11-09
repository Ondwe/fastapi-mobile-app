"""
Main application entry point - Redirects to connected business API
This ensures compatibility with existing deployment setup
"""
from main_connected_fixed import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
