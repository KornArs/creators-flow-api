from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from webapp.endpoints import users, orders
from webapp.logger import main_logger

app = FastAPI(title="Creators Flow API", description="Backend API for Creators Flow WebApp")

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
