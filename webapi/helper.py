import functools

from flask import request, jsonify

from database import SqlAlchemyORM
from shared.result import Result
from shared.valueobject import DomainError


def atomic(func):
    @functools.wraps(func)
    def wrapper():
        orm = SqlAlchemyORM()
        with orm.unit_of_work() as uow:
            setattr(request, 'uow', uow)
            response = func()

            if response[1] != 200:
                uow.rollback()
            else:
                # TODO check commit result is success
                uow.commit()

        return response

    return wrapper


def present_result(result: Result):
    """
    TODO refactor mapping result class to HTTP response code
    It does not get worse
    """

    status_code = 500
    data = {
        "result": None
    }
    if result.is_failure:
        data["result"] = False
        if isinstance(result.error, DomainError):
            if "NotFound" in result.error.message:
                status_code = 404
            elif "ResourceError" in result.error.message:
                status_code = 500
            elif "ValidationError" in result.error.message:
                status_code = 400
            else:
                status_code = 500
        else:
            status_code = 500

        data["message"] = getattr(result.error, 'message', 'Unknown')
        data["error"] = result.error.value or "Unknown"
    else:
        data["result"] = True
        status_code = 200
        if isinstance(result.value, dict):
            data.update(result.value)

    return jsonify(**data), status_code
