from typing import Dict

from auth.commands.login_user import LoginUserCommand, LoginUserCommandHandler
from auth.commands.signup_user import SignupUserCommand, SignupUserCommandHandler
from auth.abc import AuthServiceABC
from database.abc import UnitOfWorkABC
from shared.result import Result


class AuthService(AuthServiceABC):
    def __init__(self, unit_of_work: UnitOfWorkABC):
        self._uow = unit_of_work

    def signup_user(self, request_dto: Dict) -> Result:
        command_or_error = SignupUserCommand.create(request_dto)
        if command_or_error.is_failure:
            return Result.fail(command_or_error.error)

        command_handler = SignupUserCommandHandler(self._uow)
        result = command_handler.execute(command_or_error.value)

        return result

    def login_user(self, request_dto: Dict):
        command_or_error = LoginUserCommand.create(request_dto)
        if command_or_error.is_failure:
            return Result.fail(command_or_error.error)

        command_handler = LoginUserCommandHandler(self._uow)
        result = command_handler.execute(command_or_error.value)

        return result

    def get_user(self, request_dto: Dict) -> Result:
        raise NotImplemented
