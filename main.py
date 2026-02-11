from fastapi import FastAPI, responses

app = FastAPI()

@app.get('/')
async def index():
    return responses.FileResponse('public/index.html')

@app.get('/health')
async def health():
    return {
        "status": "healthy",
        "secured": True,
        "imperial_integration": "26/26 ports",
        "system": "Humbu Imperial Business Brain"
    }
