import os
from dotenv import load_dotenv

# Подгружаем .env из текущей директории (webapp/.env)
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=dotenv_path)

# Отладочная печать
print("DEBUG | MYSQL_HOST:", os.getenv("MYSQL_HOST"))

# Переменные окружения
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "test")


