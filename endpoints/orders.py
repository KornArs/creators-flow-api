from fastapi import APIRouter, HTTPException, Query 
from typing import List, Optional 
import aiomysql 
from db import get_connection, close_connection
from models import Order, OrderSummary, Video
from logger import get_logger 
 
# Создаем логгер для данного модуля 
logger = get_logger('endpoints.orders') 
 
router = APIRouter() 
 
@router.get("/orders", response_model=List[OrderSummary]) 
async def get_orders(brand_id: Optional[int] = Query(None)): 
    """Получение списка заказов с возможной фильтрацией по бренду.""" 
    logger.info(f"Requesting orders with filter: brand_id={brand_id}") 
    conn, pool = await get_connection() 
    try: 
        async with conn.cursor() as cursor: 
            query = "SELECT id, product_description, video_count, status, deadline, created_at FROM orders" 
            params = [] 
            if brand_id: 
                query += " WHERE brand_id = %s" 
                params.append(brand_id) 
            query += " ORDER BY created_at DESC" 
            logger.debug(f"Executing query: {query} with params: {params}") 
            await cursor.execute(query, params) 
            orders = await cursor.fetchall() 
            logger.info(f"Retrieved {len(orders)} orders") 
            return orders 
    except Exception as e: 
        logger.error(f"Error retrieving orders: {e}") 
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") 
    finally: 
        await close_connection(conn, pool) 
 
@router.get("/orders/{order_id}", response_model=Order) 
async def get_order(order_id: int): 
    """Получение подробной информации о заказе по ID.""" 
    logger.info(f"Requesting order with ID {order_id}") 
    conn, pool = await get_connection() 
    try: 
        async with conn.cursor() as cursor: 
            await cursor.execute("SELECT * FROM orders WHERE id = %s", (order_id,)) 
            order = await cursor.fetchone() 
            if not order: 
                logger.warning(f"Order with ID {order_id} not found") 
                raise HTTPException(status_code=404, detail=f"Order with ID {order_id} not found") 
            logger.info(f"Retrieved order with ID {order_id}") 
            return order 
    except Exception as e: 
        logger.error(f"Error retrieving order {order_id}: {e}") 
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") 
    finally: 
        await close_connection(conn, pool) 
 
@router.get("/videos", response_model=List[Video]) 
async def get_videos(creator_id: Optional[int] = Query(None), order_id: Optional[int] = Query(None)): 
    """Получение списка видео с фильтрацией по creator_id и/или order_id.""" 
    logger.info(f"Requesting videos with filters: creator_id={creator_id}, order_id={order_id}") 
    conn, pool = await get_connection() 
    try: 
        async with conn.cursor() as cursor: 
            query = "SELECT * FROM videos" 
            params = [] 
            conditions = [] 
            if creator_id: 
                conditions.append("creator_id = %s") 
                params.append(creator_id) 
            if order_id: 
                conditions.append("order_id = %s") 
                params.append(order_id) 
            if conditions: 
                query += " WHERE " + " AND ".join(conditions) 
            query += " ORDER BY uploaded_at DESC" 
            logger.debug(f"Executing query: {query} with params: {params}") 
            await cursor.execute(query, params) 
            videos = await cursor.fetchall() 
            logger.info(f"Retrieved {len(videos)} videos") 
            return videos 
    except Exception as e: 
        logger.error(f"Error retrieving videos: {e}") 
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") 
    finally: 
        await close_connection(conn, pool) 
