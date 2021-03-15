from dataclasses import dataclass
from typing import TypeVar

T = TypeVar("T")


@dataclass
class DomainError:
    message: str
    value: T


@dataclass
class UserID:
    id_: str
