from database.abc import UnitOfWorkABC
from shared.cqrs import CommandABC
from shared.result import Result
from shared.validators import String, Number
from shared.valueobject import StadiumID
from volleyball_federation.entity import Stadium


class BuildStadiumCommand(CommandABC):
    stadium_id = String(minsize=8, maxsize=32)
    name = String(minsize=2, maxsize=150)
    capacity = Number(minvalue=1)

    def __init__(self, stadium_id: str, name: str, capacity: int):
        super().__init__(stadium_id=stadium_id, name=name, capacity=capacity)


class BuildStadiumCommandHandler:
    def __init__(self, unit_of_work: UnitOfWorkABC):
        self._uow = unit_of_work

    def execute(self, command: BuildStadiumCommand):
        stadium_or_error = Stadium.create(
            stadium_id=StadiumID(command.stadium_id),
            name=command.name,
            capacity=command.capacity
        )
        if stadium_or_error.is_failure:
            return Result.fail(stadium_or_error.error)

        success_or_error = self._uow.stadium_repository.create_stadium(stadium=stadium_or_error.value)
        if success_or_error.is_failure:
            return Result.fail(stadium_or_error.error)

        return Result.ok()
