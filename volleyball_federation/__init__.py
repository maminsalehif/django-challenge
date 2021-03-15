from typing import Dict

from shared.result import Result
from volleyball_federation.abc import VolleyballFederationServiceABC
from volleyball_federation.commands.build_stadium import BuildStadiumCommand, BuildStadiumCommandHandler
from volleyball_federation.commands.create_match import CreateMatchCommand, CreateMatchCommandHandler
from volleyball_federation.commands.define_match_seats import DefineMatchSeatsCommand, DefineMatchSeatsCommandHandler
from volleyball_federation.commands.new_team import CreateTeamCommand, CreateTeamCommandHandler
from database.unit_of_work import UnitOfWorkABC


class VolleyballFederationService(VolleyballFederationServiceABC):
    def __init__(self, unit_of_work: UnitOfWorkABC):
        self._uow = unit_of_work

    def build_stadium(self, request_dto: Dict) -> Result:
        command_or_error = BuildStadiumCommand.create(request_dto)
        if command_or_error.is_failure:
            return Result.fail(command_or_error.error)

        command_handler = BuildStadiumCommandHandler(self._uow)
        result = command_handler.execute(command_or_error.value)

        return result

    def new_team(self, request_dto: Dict) -> Result:
        command_or_error = CreateTeamCommand.create(request_dto)
        if command_or_error.is_failure:
            return Result.fail(command_or_error.error)

        command_handler = CreateTeamCommandHandler(self._uow)
        result = command_handler.execute(command_or_error.value)

        return result

    def new_match(self, request_dto: Dict) -> Result:
        command_or_error = CreateMatchCommand.create(request_dto)
        if command_or_error.is_failure:
            return Result.fail(command_or_error.error)

        command_handler = CreateMatchCommandHandler(self._uow)
        result = command_handler.execute(command_or_error.value)

        return result

    def define_seats_for_match(self, request_dto: Dict) -> Result:
        command_or_error = DefineMatchSeatsCommand.create(request_dto)
        if command_or_error.is_failure:
            return Result.fail(command_or_error.error)

        command_handler = DefineMatchSeatsCommandHandler(self._uow)
        result = command_handler.execute(command_or_error.value)

        return result

    def book_seats_of_the_match(self, request_dto: Dict) -> Result:
        raise NotImplemented
