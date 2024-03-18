from time import time
from typing import Callable, TypeVar
from functools import wraps


Logger = TypeVar("Logger")


class Utils:
    logger: Logger

    @classmethod
    def get_time(cls, func: Callable[..., any]):
        @wraps(func)
        def wrapper(*args, **kwargs) -> any:
            if kwargs.get("skip"):
                return func(*args, **kwargs)
            start_time = time()
            result = func(*args, **kwargs)
            cls.logger.info(time() - start_time)
            return result
        return wrapper

