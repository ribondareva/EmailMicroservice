import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s %(asctime)s %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)