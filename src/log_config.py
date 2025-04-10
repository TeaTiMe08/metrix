import logging
import os
from pathlib import Path

# Configure logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FILE = os.getenv("LOG_FILE", None)

# Set up logging
logger = logging.getLogger()
logger.setLevel(LOG_LEVEL)

# Create formatter
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# Add console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Add file handler if LOG_FILE is specified
if LOG_FILE:
    # Make sure the directory exists
    log_path = Path(LOG_FILE)
    log_dir = log_path.parent
    os.makedirs(log_dir, exist_ok=True)

    # Clean up existing log file if requested
    if log_path.exists():
        try:
            log_path.unlink()  # Delete the existing file
            print(f"Removed existing log file: {LOG_FILE}")
        except Exception as e:
            print(f"Failed to remove existing log file: {e}")

    # Use utf-8 encoding to handle all Unicode characters
    file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8', errors='replace')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.info(f"Logging to file: {LOG_FILE}")
