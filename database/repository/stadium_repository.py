from typing import List

from sqlalchemy import and_
from sqlalchemy.orm import Session

from database.abc import StadiumRepositoryABC
from database.models import StadiumModel
from shared.result import Result
from shared.valueobject import SeatID, StadiumID, DomainError
from volleyball_federation.entity import Stadium


class StadiumRepository(StadiumRepositoryABC):
    def __init__(self, session: Session):
        self.session = session

    def create_stadium(self, stadium: Stadium) -> Result:
        self.session.add(StadiumModel.from_entity(stadium))
        return Result.ok()

    def get_stadium(self, stadium_id: StadiumID) -> Result:
        model_or_none = self.session.query(StadiumModel).filter_by(stadium_id=stadium_id.id_).one_or_none()
        if model_or_none is None:
            return Result.fail(DomainError("StadiumNotFound", None))

        return Result.ok(model_or_none.to_entity())

    def check_seats_placed_in_the_stadium(self, seat_ids: List[SeatID], stadium_id: StadiumID) -> Result:
        # TODO Oops all functions dose not work
        result = self.session.query(StadiumModel).filter(
            and_(
                StadiumModel.seats.all(list(map(lambda seat_id: seat_id.id_, seat_ids))),
                StadiumModel.stadium_id == stadium_id.id_
            )
        ).exists()

        if result is False:
            return Result.fail(DomainError("SeatsNotExists", None))

        return Result.ok(True)
