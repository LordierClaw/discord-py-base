import logging
import sys
from logging.handlers import RotatingFileHandler
from config import LOG_LEVEL, LOG_FORMAT, LOG_FILE

def setup_logger(name):
    """Create and configure a logger instance"""
    logger = logging.getLogger(name)
    
    # Set the logging level
    level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
    logger.setLevel(level)
    
    # Create formatters
    formatter = logging.Formatter(LOG_FORMAT)
    
    # Create handlers
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=5*1024*1024, backupCount=5
    )
    file_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger