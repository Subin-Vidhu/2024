"""
Logging utilities for DICOM processing
"""

import logging

def get_logger(name=__name__, level=logging.INFO):
    """
    Set up a logger with consistent formatting
    
    Args:
        name: Logger name (default: module name)
        level: Logging level (default: INFO)
    
    Returns:
        Configured logger instance
    """
    # Set up logging
    logger = logging.getLogger(name)
    
    # Only add handler if it doesn't already have one
    if not logger.handlers:
        logger.setLevel(level)
        
        # Create console handler
        handler = logging.StreamHandler()
        handler.setLevel(level)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # Add formatter to handler
        handler.setFormatter(formatter)
        
        # Add handler to logger
        logger.addHandler(handler)
    
    return logger

# Default logger
logger = get_logger('dicom_utils') 