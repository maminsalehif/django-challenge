from sqlalchemy.orm import Session

from auth.entity import UserCredential
from database.abc import UserCredentialRepositoryABC
from database.models import UserCredentialModel
from shared.result import Result
from shared.valueobject import DomainError


class UserCredentialRepository(UserCredentialRepositoryABC):
    def __init__(self, session: Session):
        self.session = session

    def create_user_credential(self, user_credential: UserCredential) -> Result:
        self.session.add(UserCredentialModel.from_entity(user_credential))
        return Result.ok()

    def get_user_credential_by_phone_number(self, phone_number: str) -> Result:
        model_or_none = self.session.query(UserCredentialModel).filter_by(phone_number=phone_number).one_or_none()
        if model_or_none is None:
            return Result.fail(DomainError("UserCredentialNotFound", None))

        return Result.ok(model_or_none.to_entity())
