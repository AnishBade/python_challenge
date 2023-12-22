import traceback

from fastapi import Request, Response, status
from loguru import logger
# from strawberry.extensions import SchemaExtension
# from v6.logger import configure_logging

# configure_logging()


def get_endpoint_info(request: Request, response: Response = None):
    if request:
        log_entry = {
            "method": request.method,
            "endpoint": request.url.path,
            "status_code": response.status_code if response else status.HTTP_400_BAD_REQUEST,
            "remote_addr": request.client.host,
        }
    else:
        log_entry = {}
    return log_entry


def log_exception(message: str = "Internal server error.", request: Request = None):
    logger.critical(
        message,
        request_detail={
            "endpoint_info": get_endpoint_info(request),
            "traceback": traceback.format_exc(),
        },
    )


async def log_endpoint(request: Request, response, elapsed_time: float):
    status_code = response.status_code
    method = request.method
    url = request.url.path
    remote_addr = request.client.host

    detail = get_endpoint_info(request, response)
    detail |= {"elapsed_time": elapsed_time}
    logger.info(
        f"{method} - {url} - {status_code} - {remote_addr} - {elapsed_time:.6f}ms",
        request_detail=detail,
    )


class PythonLoggerExtension():
    def __init__(self):
        self.logger = logger

    def log_exception(self, message: str = "Internal server error."):
        configure_logging(std_error=True)

        logger.critical(
            message,
            request_detail={
                "traceback": traceback.format_exc(),
            },
        )

    def on_request_end(self, message: str = "Internal server error."):
        traceback_str = ""
        if self.execution_context.errors:
            for error in self.execution_context.errors:
                if error.original_error:
                    trace = traceback.extract_tb(error.original_error.__traceback__).format()
                    traceback_str = "".join(trace)
                else:
                    traceback_str = error

            self.logger.critical(
                message,
                request_detail={
                    "traceback": str(traceback_str),
                },
            )
