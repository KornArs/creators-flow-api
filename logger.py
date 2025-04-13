import logging
import sys
from logging.handlers import RotatingFileHandler
import os

# Создаем директорию для логов, если её нет
os.makedirs('logs', exist_ok=True)

def setup_logger(name):
    """Настраивает и возвращает логгер с заданным именем."""
    logger = logging.getLogger(name)

    if logger.hasHandlers():
        return logger  # предотвращает дублирование хендлеров

    logger.setLevel(logging.DEBUG)

    log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    # Хендлер на stdout
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(log_format)

    # Хендлер на файл
    file_handler = RotatingFileHandler(f'logs/{name}.log', maxBytes=10 * 1024 * 1024, backupCount=5)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(log_format)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

# Создаем основной логгер
main_logger = setup_logger('webapp')

def get_logger(module_name):
    """Получает логгер для конкретного модуля"""
    return logging.getLogger(f'webapp.{module_name}')