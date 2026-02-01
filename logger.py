"""Logging system for Financial Intelligence Dashboard."""

import logging
import os
from datetime import datetime
from pathlib import Path


class DashboardLogger:
    """Centralized logging for the dashboard."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize logging system."""
        # Create logs directory if it doesn't exist
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # Create log file with timestamp
        log_file = log_dir / f"dashboard_{datetime.now().strftime('%Y%m%d')}.log"
        
        # Configure logger
        self.logger = logging.getLogger("FinancialDashboard")
        self.logger.setLevel(logging.DEBUG)
        
        # Remove existing handlers to avoid duplicates
        self.logger.handlers = []
        
        # File handler - detailed logging
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - [%(funcName)s:%(lineno)d] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_format)
        
        # Console handler - info level
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        # Force UTF-8 encoding to handle emoji/unicode characters
        if hasattr(console_handler, 'stream'):
            console_handler.stream.reconfigure(encoding='utf-8', errors='replace')
        console_format = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(console_format)
        
        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def info(self, message: str, **kwargs):
        """Log info level message."""
        self.logger.info(message, **kwargs)
    
    def debug(self, message: str, **kwargs):
        """Log debug level message."""
        self.logger.debug(message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning level message."""
        self.logger.warning(message, **kwargs)
    
    def error(self, message: str, exc_info=False, **kwargs):
        """Log error level message."""
        self.logger.error(message, exc_info=exc_info, **kwargs)
    
    def exception(self, message: str):
        """Log exception with traceback."""
        self.logger.exception(message)


def get_logger() -> DashboardLogger:
    """Get or create the dashboard logger."""
    return DashboardLogger()
