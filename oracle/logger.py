"""Global logging for the Oracle demo."""

import logging

logging.basicConfig(
    format="%(asctime)-15s %(levelname)s :: %(filename)s:%(lineno)s:%(funcName)s() :: %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%SZ",
    level="INFO",
)

logger = logging.getLogger(__name__)
