from main import app as fastapi_app

# Simple worker function - Cloudflare Python Workers beta can handle this
async def fetch(request):
    # Basic request handling for FastAPI
    return await fastapi_app(request.scope, request.receive, request.waitUntil)
