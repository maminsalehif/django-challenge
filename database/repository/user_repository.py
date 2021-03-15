from sqlalchemy.orm import Session

from auth.entity import User
from database.abc import UserRepositoryABC
from database.models import UserModel
from shared.result import Result
from shared.valueobject import UserID, DomainError


class UserRepository(UserRepositoryABC):
    def __init__(self, session: Session):
        self.session = session

    def creat_user(self, user: User) -> Result:
        self.session.add(UserModel.from_entity(user))
        return Result.ok()

    def get_user(self, user_id: UserID) -> Result:
        model_or_none = self.session.query(UserModel).filter_by(user_id=user_id.id_).one_or_none()
        if model_or_none is None:
            return Result.fail(DomainError("UserNotFound", None))

        return Result.ok(model_or_none.to_entity())

    def get_user_by_phone_number(self, phone_number: str) -> Result:
        model_or_none = self.session.query(UserModel).filter_by(phone_number=phone_number).one_or_none()
        if model_or_none is None:
            return Result.fail(DomainError("UserNotFound", None))

        return Result.ok(model_or_none.to_entity())
