import logging
import sys

from app.config.settings import settings


def _build_logger() -> logging.Logger:

    logger = logging.getLogger("neosoc")

    logger.setLevel(settings.log_level.upper())

    if not logger.handlers:

        handler = logging.StreamHandler(sys.stdout)

        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        handler.setFormatter(formatter)

        logger.addHandler(handler)

        logger.propagate = False

    return logger


logger = _build_logger()
