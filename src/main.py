import sys
from typing import Callable, Iterable

import numpy as np
from loguru import logger

from config import settings
from utils import Utils


class App:
    array_length: int = settings.ELEMENT_AMOUNT
    rows: int = settings.ROWS
    cols: int = settings.COLS
    low: int = settings.LOW
    high: int = settings.HIGH

    format: str = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <blue>{level}</blue> | {message}"

    def __init__(self) -> None:
        self.__init_logger()
        logger.info("App initializing...")
        Utils.logger = logger
        self.__array = np.random.randint(self.low, self.high, size=self.array_length)
        self.__list = list(self.__array)
        logger.info("App initialized")
        logger.info(f"Initial array: {self.__array}")
        logger.info(f"Initial list: {self.__list}")

    def run(self) -> None:
        for target in (
                self.__transform_as_2d_array,
                self.__transform_as_2d_list,
                self.__increase_array_by,
                self.__increase_list_by
        ):
            self.__default_pipeline(target=target)

    @classmethod
    def __default_pipeline(cls, target: Callable[..., Iterable[Iterable[int]]]) -> None:
        logger.info(f"Start transforming using {target.__name__}")

        logger.info("Required time:")
        result = target()
        logger.info(f"Result:")
        cls.__print_matrix(result)

    @Utils.get_time
    def __transform_as_2d_array(self) -> np.ndarray:
        self.__array = np.reshape(self.__array, newshape=(self.rows, self.cols))
        return self.__array

    @Utils.get_time
    def __transform_as_2d_list(self) -> list[list[int]]:
        new_list: list[list[int]] = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        for i, elem in enumerate(self.__list):
            new_list[i // self.cols][i % self.cols] = elem
        self.__list = new_list
        return self.__list

    @Utils.get_time
    def __increase_array_by(self, number: int = 10) -> np.ndarray:
        self.__array += number
        return self.__array

    @Utils.get_time
    def __increase_list_by(self, number: int = 10, target: list = None, **kwargs) -> list[list[int]]:
        if not target:
            target = self.__list
        for i, elem in enumerate(target):
            if isinstance(elem, list):
                self.__increase_list_by(number=number, target=elem, skip=True)
            else:
                target[i] += number
        return target

    @classmethod
    def __print_matrix(cls, matrix: Iterable[Iterable[int]]):
        for row in matrix:
            logger.info(' '.join([str(elem) for elem in row]))

    @classmethod
    def __init_logger(cls) -> None:
        logger.remove()
        logger.add(sys.stdout, format=cls.format, colorize=True, level=settings.LOG_LEVEL)
        logger.add("file.log", format=cls.format, level=settings.LOG_LEVEL)


if __name__ == "__main__":
    app = App()
    app.run()
