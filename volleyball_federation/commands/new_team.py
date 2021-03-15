from database.abc import UnitOfWorkABC
from shared.cqrs import CommandABC
from shared.result import Result
from shared.validators import String
from volleyball_federation.entity import Team, TeamID


class CreateTeamCommand(CommandABC):
    team_id = String(minsize=8, maxsize=32)
    name = String(minsize=2, maxsize=150)

    def __init__(self, team_id: str, name: str):
        super().__init__(team_id=team_id, name=name)


class CreateTeamCommandHandler:
    def __init__(self, unit_of_work: UnitOfWorkABC):
        self._uow = unit_of_work

    def execute(self, command: CreateTeamCommand):
        team_or_error = Team.create(
            team_id=TeamID(command.team_id),
            name=command.name
        )
        if team_or_error.is_failure:
            return Result.fail(team_or_error.error)

        success_or_error = self._uow.team_repository.create_team(team=team_or_error.value)
        if success_or_error.is_failure:
            return Result.fail(team_or_error.error)

        return Result.ok()
