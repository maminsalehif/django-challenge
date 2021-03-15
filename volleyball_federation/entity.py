from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from shared.result import Result
from shared.valueobject import StadiumID, SeatID, TeamID, MatchID, DomainError

"""
Stadium Aggregate(DDD)
"""


@dataclass
class Stadium:
    """
    Aggregate root
    """
    stadium_id: StadiumID
    name: str
    seats: List['Seat'] = field(default_factory=list)

    @staticmethod
    def create(**kwargs):
        seats = _generate_seats_base_on_capacity(kwargs.pop('capacity'))
        return Result.ok(Stadium(seats=seats, **kwargs))


def _generate_seats_base_on_capacity(capacity):
    """
    im using simplest id generator for seats.
    Because Seat is a local entity for stadium aggregate root,
    so SeatID dose not have to be unique in whole system.
    """
    return [Seat(SeatID(id_=f"SEAT{i + 1}")) for i in range(capacity)]


@dataclass
class Seat:
    seat_id: SeatID


"""
Team Aggregate
"""


@dataclass
class Team:
    team_id: TeamID
    name: str

    @staticmethod
    def create(**kwargs):
        return Result.ok(Team(**kwargs))


"""
Volleyball Match Aggregate
"""


@dataclass
class Match:
    match_id: MatchID
    host_team_id: TeamID
    guest_team_id: TeamID
    stadium_id: StadiumID
    time: datetime
    stadium_seats: List[SeatID] = field(default_factory=list)

    @staticmethod
    def create(**kwargs):
        if kwargs['host_team_id'] == kwargs['guest_team_id']:
            return Result.fail(DomainError("TeamsAreTheSame", None))

        return Result.ok(Team(**kwargs))
