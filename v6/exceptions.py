from functools import wraps
from typing import Callable

from fastapi import status
from utils.logger import log_exception


class PythonHttpException(Exception):
    def __init__(
        self,
        message: str,
        status: int = status.HTTP_400_BAD_REQUEST,
        detail: str | dict | list = "",
    ):
        self.message = message
        self.status = status
        self.detail = detail
        super().__init__(message)


def handle_exceptions(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            response = await func(*args, **kwargs)
        except Exception as e:
            request = kwargs.get("request")
            log_exception(message=str(e), request=request)
            raise PythonHttpException(
                message=str(e),
                status=status.HTTP_400_BAD_REQUEST,
                detail=e,
            )
        else:
            return response

    return wrapper


class SomethingWentWrong(Exception):
    pass
