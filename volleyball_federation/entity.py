from dataclasses import dataclass, field
from typing import List

from shared.valueobject import StadiumID, SeatID

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
    seats: List[SeatID] = field(default_factory=list)


class Seat:
    seat_id: SeatID
