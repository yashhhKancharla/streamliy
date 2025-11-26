"""
Logging Configuration
Grounded_In: Assignment - 1.pdf
"""

import sys
import structlog
from pathlib import Path
import logging


def setup_logging(log_level: str = "INFO", log_dir: Path = Path("logs")):
    """
    Configure structured logging.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_dir: Directory for log files
    """
    # Create log directory
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
    
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, log_level.upper())
    )
    
    # File handler for application logs
    file_handler = logging.FileHandler(log_dir / "app.log")
    file_handler.setLevel(getattr(logging, log_level.upper()))
    logging.getLogger().addHandler(file_handler)
    
    # Error log handler
    error_handler = logging.FileHandler(log_dir / "error.log")
    error_handler.setLevel(logging.ERROR)
    logging.getLogger().addHandler(error_handler)
