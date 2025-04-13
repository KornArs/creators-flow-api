import aiomysql
from logger import get_logger
from settings import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE

logger = get_logger("db")

DB_CONFIG = {
    "host": MYSQL_HOST,
    "port": MYSQL_PORT,
    "user": MYSQL_USER,
    "password": MYSQL_PASSWORD,
    "db": MYSQL_DATABASE,
}

async def get_pool():
    try:
        pool = await aiomysql.create_pool(
            **DB_CONFIG,
            charset="utf8mb4",
            cursorclass=aiomysql.DictCursor,
            maxsize=10
        )
        logger.info("Database connection pool created")
        return pool
    except Exception as e:
        logger.error(f"Error creating connection pool: {e}")
        raise

async def get_connection():
    try:
        pool = await get_pool()
        conn = await pool.acquire()
        logger.debug("Database connection acquired from pool")
        return conn, pool
    except Exception as e:
        logger.error(f"Error getting connection from pool: {e}")
        raise

async def close_connection(conn, pool):
    try:
        pool.release(conn)
        logger.debug("Connection released")
        pool.close()
        await pool.wait_closed()
        logger.debug("Connection pool closed")
    except Exception as e:
        logger.error(f"Error closing connection: {e}")
