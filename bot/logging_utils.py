import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

def setup_logging():
    """Setup comprehensive logging system"""
    
    # Create logs directory if it doesn't exist
    log_dir = os.path.join(os.getcwd(), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # Create logger
    logger = logging.getLogger('web_bot')
    logger.setLevel(logging.INFO)
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # File handler with rotation (10MB max, keep 5 files)
    log_file = os.path.join(log_dir, 'bot_sessions.log')
    file_handler = RotatingFileHandler(
        log_file, 
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)8s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def log_session_stats(session_num, success, duration, proxy_ip=None, pages_visited=0, errors=None):
    """Log detailed session statistics"""
    logger = logging.getLogger('web_bot')
    
    stats = {
        'session': session_num,
        'success': success,
        'duration_minutes': round(duration, 1),
        'proxy_ip': proxy_ip,
        'pages_visited': pages_visited,
        'errors': errors or []
    }
    
    if success:
        logger.info(f"Session-{session_num} SUCCESS | {duration:.1f}min | {pages_visited} pages | IP: {proxy_ip}")
    else:
        logger.error(f"Session-{session_num} FAILED | {duration:.1f}min | Errors: {errors}")
    
    return stats
