from abc import ABCMeta
from typing import Dict

from shared.valueobject import DomainError
from shared.result import Result

"""
    Command and Query class assures the handler that the request DTO is valid.    
"""


class CommandABC(metaclass=ABCMeta):

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def create(cls, a_dict: Dict) -> Result:
        try:
            command = cls(**a_dict)
            return Result.ok(command)
        except (TypeError,ValueError) as e:
            return Result.fail(DomainError("ValidationError", e))


class QueryABC(metaclass=ABCMeta):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def create(cls, a_dict: Dict) -> Result:
        try:
            command = cls(**a_dict)
            return Result.ok(command)
        except ValueError as e:
            return Result.fail(DomainError("ValidationError", e))
