from abc import ABCMeta, abstractmethod
from typing import List

from auth.entity import User, UserCredential
from shared.result import Result
from shared.valueobject import UserID, StadiumID, TeamID
from volleyball_federation.entity import Stadium, Team


class UnitOfWorkABC(metaclass=ABCMeta):
    """
    Unit of work(UOW) track changes in database
    UOW is responsible for atomic transaction
    https://martinfowler.com/eaaCatalog/unitOfWork.html

    Command handlers can access to repositories from uow
    """

    @abstractmethod
    def __enter__(self): pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb): pass

    @abstractmethod
    def commit(self): pass

    @abstractmethod
    def rollback(self): pass

    @property
    @abstractmethod
    def user_repository(self) -> 'UserRepositoryABC': pass

    @property
    @abstractmethod
    def user_credential_repository(self) -> 'UserCredentialRepositoryABC': pass

    @property
    @abstractmethod
    def stadium_repository(self) -> 'StadiumRepositoryABC': pass

    @property
    @abstractmethod
    def team_repository(self) -> 'TeamRepositoryABC': pass


class UserRepositoryABC(metaclass=ABCMeta):
    """
    Repository classes responsible for:
      - convert entities to database models
      - store models in db

    There is one repository for each Aggregate root(DDD)
    """

    def creat_user(self, user: User) -> Result: pass

    def get_user(self, user_id: UserID) -> Result: pass

    def get_user_by_phone_number(self, phone_number: str) -> Result: pass


class UserCredentialRepositoryABC(metaclass=ABCMeta):
    def create_user_credential(self, user_credential: UserCredential) -> Result: pass

    def get_user_credential_by_phone_number(self, phone_number: str) -> Result: pass


class StadiumRepositoryABC(metaclass=ABCMeta):
    def create_stadium(self, stadium: Stadium) -> Result: pass

    def get_stadium(self, stadium_id: StadiumID) -> Result: pass

    def check_seats_placed_in_the_stadium(self, seat_ids: List[StadiumID]) -> Result: pass


class TeamRepositoryABC(metaclass=ABCMeta):
    def create_team(self, team: Team) -> Result: pass

    def get_team(self, team_id: TeamID) -> Result: pass
