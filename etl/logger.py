import sys

from loguru import logger

LOGGING_FORMAT = (
    '<green>[{time:YYYY-MM-DD HH:mm:ss.SSS}]</green> | '
    '<level>{level: <8}</level> | '
    '<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level> | '
    '{extra}'
)

logger.remove()
logger.add(sys.stdout, format=LOGGING_FORMAT)


__all__ = ['logger']
