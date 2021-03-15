from typing import List

from sqlalchemy import and_
from sqlalchemy.orm import Session

from database.abc import MatchRepositoryABC
from database.models import MatchModel
from shared.result import Result
from shared.valueobject import SeatID, MatchID, DomainError
from volleyball_federation.entity import Match


class MatchRepository(MatchRepositoryABC):
    def __init__(self, session: Session):
        self.session = session

    def create_match(self, match: Match) -> Result:
        self.session.add(MatchModel.from_entity(match))
        return Result.ok()

    def get_match(self, match_id: MatchID) -> Result:
        model_or_none = self.session.query(MatchModel).filter_by(match_id=match_id.id_).one_or_none()
        if model_or_none is None:
            return Result.fail(DomainError("MatchNotFound", None))

        return Result.ok(model_or_none.to_entity())

    def add_new_seats_for_the_match(self, seat_ids: List[SeatID], match_id: MatchID) -> Result:
        model_or_none = self.session.query(MatchModel).filter_by(match_id=match_id.id_).one_or_none()
        if model_or_none is None:
            return Result.fail(DomainError("MatchNotFound", None))

        model_or_none.stadium_seats.extend(list(map(lambda seat_id: seat_id.id_, seat_ids)))
        return Result.ok()

    def check_seats_placed_in_the_match(self, seat_ids: List[SeatID], match_id: MatchID) -> Result:
        result = self.session.query(MatchModel).filter(
            and_(
                MatchModel.stadium_seats.all(list(map(lambda seat_id: seat_id.id_, seat_ids))),
                MatchModel.match_id == match_id.id_
            )
        ).exists()

        if not result:
            return Result.fail(DomainError("SeatsNotExists", None))

        return Result.ok(True)
