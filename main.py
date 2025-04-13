from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from endpoints import users, orders
from logger import main_logger

app = FastAPI(
    title="Creators Flow API",
    description="Backend API for Creators Flow WebApp",
    version="0.1.0"
)

# --- Swagger API Key support ---
from fastapi.openapi.utils import get_openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Creators Flow API",
        version="0.1.0",
        description="Backend API for Creators Flow WebApp",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "APIKeyHeader": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization"
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"APIKeyHeader": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
# --------------------------------

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        main_logger.info(f"Request started: {request.method} {request.url.path}")
        response = await call_next(request)
        duration = time.time() - start_time
        main_logger.info(f"Request completed: {request.method} {request.url.path} "
                         f"Status: {response.status_code} Duration: {duration:.4f}s")
        return response

app.add_middleware(LoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/api", tags=["Users"])
app.include_router(orders.router, prefix="/api", tags=["Orders"])

@app.get("/")
async def root():
    main_logger.info("Root endpoint called")
    return {"message": "Welcome to Creators Flow API"}

@app.on_event("startup")
async def startup_event():
    main_logger.info("Application startup")

@app.on_event("shutdown")
async def shutdown_event():
    main_logger.info("Application shutdown")

if __name__ == "__main__":
    main_logger.info("Starting application")
    uvicorn.run("webapp.main:app", host="0.0.0.0", port=8000, reload=True)