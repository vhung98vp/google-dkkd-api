import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set logging level (INFO, DEBUG, ERROR, etc.)
    format="%(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),  # Send logs to stdout
    ],
)

def get_logger(name):
    """
    Returns a logger instance with the given name.
    """
    return logging.getLogger(name)

