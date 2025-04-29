"""
Logging module for the Resume Rating App.

This module provides a centralized logging configuration for 
consistent logging across all parts of the application.
"""
import logging
import os
import sys
from datetime import datetime

def setup_logger(name="resume_rating", log_level=logging.INFO, log_to_file=True, log_dir="logs"):
    """
    Set up and configure a logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    if logger.hasHandlers():
        logger.handlers.clear()

    fmt = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    )
    # Console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    if log_to_file:
        os.makedirs(log_dir, exist_ok=True)
        fn = datetime.now().strftime(f"{name}_%Y%m%d.log")
        fh = logging.FileHandler(os.path.join(log_dir, fn))
        fh.setFormatter(fmt)
        logger.addHandler(fh)

    return logger

# root app logger
app_logger = setup_logger()

def get_logger(module_name: str):
    """Get a child logger for a specific module."""
    return logging.getLogger(f"resume_rating.{module_name}")
