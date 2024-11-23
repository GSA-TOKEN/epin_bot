import logging
from config.settings import LOG_LEVEL

def setup_logger():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=getattr(logging, LOG_LEVEL)
    )
    return logging.getLogger(__name__)
