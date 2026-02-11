from fastapi import FastAPI, responses; app = FastAPI(); @app.get('/')
async def index(): return responses.FileResponse('public/index.html')
