from auth.entity import UserCredential, User
from database.abc import UnitOfWorkABC
from shared.cqrs import CommandABC
from shared.valueobject import DomainError
from shared.result import Result
from shared.validators import String
from shared.valueobject import UserID


class SignupUserCommand(CommandABC):
    # TODO change String validator class by UserID value object
    user_id = String(minsize=8, maxsize=36)
    phone_number = String(minsize=11, maxsize=11)
    fullname = String(minsize=2, maxsize=50)
    password = String(minsize=8, maxsize=32)

    def __init__(self, phone_number: str, password: str):
        super().__init__(phone_number=phone_number, password=password)


class SignupUserCommandHandler:
    def __init__(self, unit_of_work: UnitOfWorkABC):
        self._uow = unit_of_work

    def execute(self, command: SignupUserCommand):
        user_or_error = self._uow.user_repository.get_user_by_phone_number(
            phone_number=command.phone_number
        )
        if user_or_error.is_success:
            return Result.fail(DomainError("PhoneNumberAlreadyExist", None))

        user = User.create(
            user_id=UserID(id_=user_or_error.value.user_id),
            phone_number=user_or_error.value.phone_number,
            fullname=user_or_error.value.fullname
        )
        # TODO hash password
        user_credential = UserCredential.create(
            user_id=user.user_id,
            phone_number=user.phone_number,
            hashed_password=user_or_error.value.password
        )

        success_or_error = self._uow.user_credential_repository.create_user_credential(user_credential)
        if success_or_error.is_failure:
            return Result.fail(success_or_error.error)

        success_or_error = self._uow.user_repository.creat_user(user=user)
        if success_or_error.is_failure:
            return Result.fail(success_or_error.error)

        return Result.ok()
