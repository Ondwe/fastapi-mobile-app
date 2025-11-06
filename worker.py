from fastapi import FastAPI
from main import app as fastapi_app

# Cloudflare Workers Python adapter
try:
    from cloudflare_workers import HttpService
    http_service = HttpService(fastapi_app)
    
    async def fetch(request):
        return await http_service.handle_request(request)
        
except ImportError:
    # Fallback for local development
    async def fetch(request):
        return Response("Cloudflare Workers Python adapter not available", status=500)
