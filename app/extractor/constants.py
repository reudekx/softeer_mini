from enum import Enum
from typing import Callable
from .parser import fotmob, fbref

SAVE_PATH = "data/{site}/html/{name}_{date}.html"


class Site(Enum):
    FOTMOB = ("fotmob", fotmob.parse)
    FBREF = ("fbref", fbref.parse)

    def __init__(self, value: str, parse: Callable[[str], dict]):
        self._value_ = value
        self.parse = parse
