from database.abc import UnitOfWorkABC
from shared.cqrs import CommandABC
from shared.valueobject import DomainError
from shared.result import Result
from shared.validators import String


class LoginUserCommand(CommandABC):
    phone_number = String(minsize=11, maxsize=11)
    password = String(minsize=8, maxsize=32)

    def __init__(self, phone_number: str, password: str):
        super().__init__(phone_number=phone_number, password=password)


class LoginUserCommandHandler:
    def __init__(self, unit_of_work: UnitOfWorkABC):
        self._uow = unit_of_work

    def execute(self, command: LoginUserCommand):
        user_or_error = self._uow.user_credential_repository.get_user_credential_by_phone_number(
            phone_number=command.phone_number
        )
        if user_or_error.is_failure:
            return Result.fail(DomainError("WrongPhoneNumberOrPassword", None))

        # TODO check hashed password
        if command.password != user_or_error.value.hashed_password:
            return Result.fail(DomainError("WrongPhoneNumberOrPassword", None))

        # Warning: login usecase is not an command in CQRS pattern
        # TODO create jwt token
        # fake jwt
        jwt = f"JWT {user_or_error.value.user_id.id_}"
        return Result.ok(jwt)
