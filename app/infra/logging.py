import logging
import os
import sys
from functools import cache

import json_logging
from fastapi.applications import FastAPI


def set_logging_webapp(app: FastAPI):
    json_logging.init_fastapi(enable_json=True)
    json_logging.init_request_instrument(app)


def set_logging_nonwebapp():
    json_logging.init_non_web(enable_json=True)


@cache
def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    log_level = os.getenv("LOG_LEVEL") or logging.INFO
    logger.setLevel(log_level)
    logger.addHandler(logging.StreamHandler(sys.stdout))
    return logger
