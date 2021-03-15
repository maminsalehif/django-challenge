from abc import ABCMeta, abstractmethod
from typing import Dict

from shared.result import Result


class VolleyballFederationServiceABC(metaclass=ABCMeta):

    @abstractmethod
    def build_stadium(self, request_dto: Dict) -> Result: pass

    @abstractmethod
    def new_team(self, request_dto: Dict) -> Result: pass

    @abstractmethod
    def new_match(self, request_dto: Dict) -> Result: pass

    @abstractmethod
    def book_seats_of_the_match(self, request_dto: Dict) -> Result: pass
