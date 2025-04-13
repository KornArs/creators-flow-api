from fastapi import APIRouter, HTTPException, Query, Request, Depends
from typing import List
from db import get_connection, close_connection
from models import User
from logger import get_logger

from auth import verify_token

logger = get_logger("endpoints.users")
router = APIRouter()

@router.get("/users", response_model=List[User])
async def get_users(request: Request, token_check=Depends(verify_token)):
    logger.info("Requesting all users")
    conn = pool = None
    try:
        conn, pool = await get_connection()
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT * FROM users_bot")
            users = await cursor.fetchall()
            return users
    except Exception as e:
        logger.error(f"Error retrieving users: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    finally:
        if conn and pool:
            await close_connection(conn, pool)

@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int, request: Request, token_check=Depends(verify_token)):
    logger.info(f"Requesting user with ID {user_id}")
    conn = pool = None
    try:
        conn, pool = await get_connection()
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT * FROM users_bot WHERE id = %s", (user_id,))
            user = await cursor.fetchone()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return user
    except Exception as e:
        logger.error(f"Error retrieving user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    finally:
        if conn and pool:
            await close_connection(conn, pool)
