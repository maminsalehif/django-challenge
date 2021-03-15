from sqlalchemy import exc

from database.abc import UnitOfWorkABC
from database.repository.match_repository import MatchRepository
from database.repository.stadium_repository import StadiumRepository
from database.repository.team_repository import TeamRepository
from database.repository.user_credential_repository import UserCredentialRepository
from database.repository.user_repository import UserRepository
from shared.result import Result
from shared.valueobject import DomainError


class AlchemyUnitOfWork(UnitOfWorkABC):
    def __init__(self, session_maker):
        self._session_maker = session_maker

    def __enter__(self):
        self._session = self._session_maker()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._session.remove()

    @property
    def user_repository(self) -> 'UserRepository':
        return UserRepository(self._session)

    @property
    def user_credential_repository(self) -> 'UserCredentialRepository':
        return UserCredentialRepository(self._session)

    @property
    def stadium_repository(self) -> 'StadiumRepository':
        return StadiumRepository(self._session)

    @property
    def team_repository(self) -> 'TeamRepository':
        return TeamRepository(self._session)

    @property
    def match_repository(self) -> 'MatchRepository':
        return MatchRepository(self._session)

    def commit(self) -> Result:
        try:
            self._session.commit()
            return Result.ok()
        except exc.SQLAlchemyError as e:
            return Result.fail(DomainError("ResourceError", e))

    def rollback(self):
        self._session.rollback()
