from dataclasses import dataclass
from typing import Generic, TypeVar, Any, List

T = TypeVar("T")


@dataclass
class Result(Generic[T]):
    """
    This class used to avoiding exception handling in each line of code
    I love it because i feel my code was cleaned by using it.

    https://khalilstemmler.com/articles/enterprise-typescript-nodejs/handling-errors-result-class/
    """

    is_success: bool
    error: T = None
    _value: T = None

    def __post_init__(self):
        if self.is_success and self.error:
            raise ValueError("InvalidOperation: A result cannot be successful and contain an error")

        if not self.is_success and not self.error:
            raise ValueError("InvalidOperation: A failing result needs to contain an error message")

    @property
    def value(self) -> T:
        if not self.is_success:
            return self.error

        return self._value

    @property
    def is_failure(self) -> bool:
        return not self.is_success

    @staticmethod
    def ok(value: T = None) -> 'Result[T]':
        return Result[T](is_success=True, error=None, _value=value)

    @staticmethod
    def fail(error: Any) -> 'Result[T]':
        return Result[T](is_success=False, error=error)

    @staticmethod
    def combine(results: List['Result']) -> 'Result[Any]':
        for result in results:
            if not isinstance(result, Result):
                continue

            if result.is_failure:
                return result

        return Result[Any].ok()

    def __repr__(self):
        return f"{'Success' if self.is_success else 'Fail'} Result(value={self.value})"

    __str__ = __repr__
