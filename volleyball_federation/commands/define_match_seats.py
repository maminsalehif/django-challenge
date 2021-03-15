from database.abc import UnitOfWorkABC
from shared.cqrs import CommandABC
from shared.result import Result
from shared.validators import String, List
from shared.valueobject import MatchID, DomainError, SeatID


class DefineMatchSeatsCommand(CommandABC):
    match_id = String(minsize=8, maxsize=32)
    seat_ids = List(minlength=1)

    def __init__(self, match_id: str, seat_ids: list):
        super().__init__(match_id=match_id, seat_ids=seat_ids)


class DefineMatchSeatsCommandHandler:
    def __init__(self, unit_of_work: UnitOfWorkABC):
        self._uow = unit_of_work

    def execute(self, command: DefineMatchSeatsCommand) -> Result:
        match_or_error = self._uow.match_repository.get_match(match_id=MatchID(command.match_id))
        if match_or_error.is_failure:
            return Result.fail(DomainError("MatchNotFound", None))

        new_seats = list(map(SeatID, command.seat_ids))
        check_seats_result = self._uow.stadium_repository.check_seats_placed_in_the_stadium(
            seat_ids=new_seats,
            stadium_id=match_or_error.value.stadium_id
        )
        if check_seats_result.is_failure:
            return Result.fail(DomainError("InvalidSeatIDs", None))

        success_or_error = self._uow.match_repository.add_new_seats_for_the_match(
            seat_ids=new_seats, match_id=match_or_error.value.match_id
        )
        if success_or_error.is_failure:
            return Result.fail(DomainError("ResourceError", None))

        return Result.ok()
