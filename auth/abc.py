from abc import ABCMeta, abstractmethod
from typing import Dict

from shared.result import Result


class AuthServiceABC(metaclass=ABCMeta):

    @abstractmethod
    def signup_user(self, request_dto: Dict) -> Result: pass

    @abstractmethod
    def login_user(self, request_dto: Dict) -> Result: pass

    @abstractmethod
    def get_user(self, request_dto: Dict) -> Result: pass
