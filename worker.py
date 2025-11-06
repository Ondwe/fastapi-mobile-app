from workers import WorkerEntrypoint
from main import app as fastapi_app
import asgi

class Default(WorkerEntrypoint):
    async def fetch(self, request):
        return await asgi.fetch(fastapi_app, request, self.env)
