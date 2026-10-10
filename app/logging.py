"""Настройка прикладного логгирования через Loguru."""

from pathlib import Path
import sys

from loguru import logger

from app.config import settings

_is_configured = False


def configure_logging() -> None:
    """Настроить консольный и файловый обработчики Loguru один раз на процесс."""
    global _is_configured
    if _is_configured:
        return

    log_path = Path(settings.log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    logger.remove()
    logger.add(
        sys.stderr,
        level=settings.log_level,
        format=(
            "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level:<8} | {name}:{function}:{line} | {message}"
        ),
    )
    logger.add(
        log_path,
        level="DEBUG",
        rotation=settings.log_rotation,
        retention=settings.log_retention,
        compression="zip",
        enqueue=True,
        backtrace=False,
        diagnose=False,
        format=(
            "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level:<8} | {name}:{function}:{line} | {message}"
        ),
    )
    _is_configured = True
