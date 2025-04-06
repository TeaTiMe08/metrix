import logging
import os

# Configure logging
LOG_LEVEL = os.getenv("LOG_LEVEL").upper()
logging.basicConfig(level=LOG_LEVEL, format="%(asctime)s - %(levelname)s - %(message)s", force=True)
logger = logging.getLogger()
