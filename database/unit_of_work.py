from sqlalchemy import exc

from database.abc import UnitOfWorkABC
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
    def user_repository(self) -> 'UserRepositoryABC':
        pass

    @property
    def user_credential_repository(self) -> 'UserCredentialRepositoryABC':
        pass

    @property
    def stadium_repository(self) -> 'StadiumRepositoryABC':
        pass

    @property
    def team_repository(self) -> 'TeamRepositoryABC':
        pass

    @property
    def match_repository(self) -> 'MatchRepositoryABC':
        pass

    def commit(self) -> Result:
        try:
            self._session.commit()
            return Result.ok()
        except exc.SQLAlchemyError as e:
            return Result.fail(DomainError("ResourceError", e))

    def rollback(self):
        self._session.rollback()
