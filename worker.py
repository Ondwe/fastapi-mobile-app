from fastapi import FastAPI
from main import app
import asyncio

async def fetch(request):
    return await app(request)
