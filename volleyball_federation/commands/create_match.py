from datetime import datetime
from typing import Union

from shared.cqrs import CommandABC
from shared.result import Result
from shared.validators import String, Timestamp
from shared.valueobject import DomainError, TeamID, StadiumID, MatchID
from volleyball_federation.entity import Match


class CreateMatchCommand(CommandABC):
    match_id = String(minsize=8, maxsize=36)
    host_team_id = String(minsize=8, maxsize=36)
    guest_team_id = String(minsize=8, maxsize=36)
    stadium_id = String(minsize=8, maxsize=36)
    time = Timestamp()

    def __init__(self, match_id: str, host_team_id: str, guest_team_id: str, stadium_id: str, time: Union[int, float]):
        super().__init__(
            match_id=match_id, host_team_id=host_team_id, guest_team_id=guest_team_id, stadium_id=stadium_id,
            time=time
        )


class CreateMatchCommandHandler:
    def __init__(self, unit_of_work):
        self._uow = unit_of_work

    def execute(self, command: CreateMatchCommand) -> Result:
        host_team_or_error = self._uow.team_repository.get_team(team_id=TeamID(command.host_team_id))
        if host_team_or_error.is_failure:
            return Result.fail(DomainError("HostTeamNotFound", None))

        guest_team_or_error = self._uow.team_repository.get_team(team_id=TeamID(command.guest_team_id))
        if guest_team_or_error.is_failure:
            return Result.fail(DomainError("GuestTeamNotFound", None))

        stadium_or_error = self._uow.stadium_repository.get_stadium(stadium_id=StadiumID(command.stadium_id))
        if stadium_or_error.is_failure:
            return Result.fail(DomainError("StadiumNotFound", None))

        match_or_error = Match.create(
            match_id=MatchID(command.match_id),
            host_team_id=host_team_or_error.value.team_id,
            guest_team_id=guest_team_or_error.value.team_id,
            stadium_id=stadium_or_error.value.stadium_id,
            time=datetime.fromtimestamp(command.time)
        )
        if match_or_error.is_failure:
            return Result.fail(match_or_error.error)

        success_or_error = self._uow.match_repository.create_match(match=match_or_error.value)
        if success_or_error.is_failure:
            return Result.fail(DomainError("ResourceError", success_or_error.error))

        return Result.ok()
