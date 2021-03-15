from dataclasses import dataclass

from shared.result import Result
from shared.valueobject import UserID


@dataclass
class User:
    user_id: UserID
    phone_number: str
    fullname: str

    @staticmethod
    def create(**kwargs):
        return Result.ok(User(**kwargs))


@dataclass
class UserCredential:
    user_id: UserID
    phone_number: str
    # TODO using ValueObject(DDD) for password
    hashed_password: str

    @staticmethod
    def create(**kwargs):
        return Result.ok(UserCredential(**kwargs))
