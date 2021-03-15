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


@dataclass
class StadiumID:
    id_: str


@dataclass
class SeatID:
    id_: str


@dataclass
class TeamID:
    id_: str


@dataclass
class MatchID:
    id_: str
