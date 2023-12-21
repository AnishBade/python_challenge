
import traceback
from loguru import logger

import json
import os
import sys

from datetime import datetime


def formatter(record):
    # data = serialize_log(record)
    record["extra"]["serialized"] = serialize_log(record)
    return "{extra[serialized]}\n"


def std_error_log_formatter(record):
    return "{extra[request_detail][traceback]}\n"


def configure_logging():
    # logger.add(sys.stderr, serialize=True)
    # logger.add(sys.stderr, format=formatter)
    logger.remove()

    logger.add(sys.stdout, level="DEBUG")

    logger.add(sys.stderr, level="CRITICAL", format=std_error_log_formatter)

    path = os.path.dirname(__file__)
    logger.add(
        f"{path}/logs/url_"
        f"{datetime.now().strftime('%Y%m%d%H%M%S')}log.json",
        rotation="50 MB",
        retention="10 days",
        level="DEBUG",
        format=formatter,
    )


configure_logging()


def log_exception(message: str = "Internal server error."):
    logger.critical(
        str(message)[:100],
        request_detail={
            "traceback": traceback.format_exc(),
        },
    )


def get_traceback_info(traceback_str: str) -> tuple:
    """Parse the traceback string to find the module_name and file_name

    Args:
        traceback_str (str): traceback string

    Returns:
        tuple: (module_name, file_name)

    """

    module_name = file_name = None

    if traceback_str:
        for line in traceback_str.splitlines():
            if line.startswith("  File "):
                file_path = line.split('"')[1]

        file_name = file_path.rsplit("/")
        module_name = file_path
        file_name = file_name[-1]

    return module_name, file_name


def serialize_log(record):
    module_name, file_name = get_traceback_info(
        record["extra"].get("request_detail", {}).get("traceback", "")
    )
    subset = {
        "level": record["level"].name,
        "time": {
            "timestamp": record["time"].timestamp(),
            "time": str(record["time"]),
        },
        "module": module_name or record["module"],
        "name": file_name or record["name"],
        # "exception": record["exception"],
        "message": record["message"],
        "file": {
            "name": record["file"].name,
            "path": record["file"].path,
        },
        "process": {
            "pid": record["process"].id,
            "name": record["process"].name,
        },
        "thread": {
            "id": record["thread"].id,
            "name": record["thread"].name,
        },
        "extra": record["extra"],
    }
    return json.dumps(subset)
