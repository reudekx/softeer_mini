from enum import Enum
from typing import Callable
from app.core import fbref_parser, fotmob_parser

SAVE_PATH = "data/{site}/html/{name}_{date}.html"


class Site(Enum):
    FOTMOB = ("fotmob", fotmob_parser.parse)
    FBREF = ("fbref", fbref_parser.parse)

    def __init__(self, value: str, parse: Callable[[str], dict]):
        self._value_ = value
        self.parse = parse
