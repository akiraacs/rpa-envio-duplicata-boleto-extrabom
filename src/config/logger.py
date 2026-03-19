import sys
from pathlib import Path

from loguru import logger

LOG_PATH = Path("logs/logs_{time:DD_MM_YYYY}.log")

# Logger remove default handler
logger.remove()

# Logger file
logger.add(
    sink=LOG_PATH, 
    rotation="1 day",
    level="INFO",
    retention=30
)

# Logger stdout
logger.add(
    sink    =sys.stdout,
    level   ="DEBUG"
)