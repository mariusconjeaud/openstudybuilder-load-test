import logging
import os
from typing import Optional


def get_logger(name: str = "Locust"):
    loglevel = os.environ.get("LOG_LEVEL", "INFO")
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {loglevel}")
    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s - %(name)-17s - %(levelname)s - %(message)s",
    )
    return logging.getLogger(name)


logger = get_logger(os.path.basename(__file__))


def load_env(key: str, default: Optional[str] = None):
    value = os.environ.get(key)
    logger.info("ENV variable fetched: %s=%s", key, value)
    if value is None and default is None:
        logger.error("%s is not set and no default was provided", key)
        raise EnvironmentError(f"Failed because {key} is not set.")
    if value is not None:
        return value
    logger.warning("%s is not set, using default value: %s", key, default)
    return default


API_BASE_URL = load_env("API_BASE_URL", "http://localhost:8000")

API_HEADERS = {
    "Authorization": f'Bearer {load_env("API_AUTH_TOKEN")}',
    "User-Agent": "Locust",
}
