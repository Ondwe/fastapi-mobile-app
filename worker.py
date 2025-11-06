from fastapi import FastAPI
import asyncio
from main import app

# Cloudflare Workers expect this exact function signature
async def on_fetch(request, env, ctx):
    return await app(request.scope, request.receive, request.waitUntil)
