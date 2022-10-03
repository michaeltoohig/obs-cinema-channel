import asyncio
from enum import Enum
from functools import wraps

import click

from cinema_playout.database.session import Session


def use_db_session(func):
    @wraps(func)
    def wrapper_func(*args, **kwargs):
        with Session() as db_session:
            func(db_session, *args, **kwargs)

    return wrapper_func


def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


class EnumType(click.Choice):
    def __init__(self, enum: Enum, case_sensitive=False):
        self.__enum = enum
        super().__init__(choices=[item.value for item in enum], case_sensitive=case_sensitive)

    def convert(self, value, param, ctx):
        if value is None or isinstance(value, Enum):
            return value

        converted_str = super().convert(value, param, ctx)
        return self.__enum(converted_str)
