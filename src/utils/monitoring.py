from loguru import logger
import time
from functools import wraps

def log_execution_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        execution_time = time.time() - start_time
        
        logger.info(f"{func.__name__} executed in {execution_time:.2f} seconds")
        return result
    return wrapper

def setup_logging():
    """Setup comprehensive logging"""
    logger.add("logs/app.log", rotation="10 MB", retention="30 days")
    logger.add("logs/errors.log", level="ERROR", rotation="10 MB")