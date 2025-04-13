from fastapi import Request, HTTPException, status, Depends
import os

API_TOKEN = os.getenv("API_TOKEN")

def verify_token(request: Request):
    token = request.headers.get("Authorization")
    if token != f"Bearer {API_TOKEN}":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token"
        )