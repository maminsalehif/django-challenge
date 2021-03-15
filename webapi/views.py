from uuid import uuid4

from flask import Blueprint, request, jsonify

from auth import AuthService
from shared.result import Result
from volleyball_federation import VolleyballFederationService
from webapi.helper import present_result, atomic

api_bp = Blueprint("volleyball", __name__, url_prefix="/api")

"""
i used verbs in url endpoints because it is more compatible with the concept of DDD
 and is cleaner than using the name.
"""


@api_bp.route("/auth/signup", methods=["POST"])
@atomic
def register_user():
    user_id = str(uuid4())
    request_dto = {
        **request.get_json(),
        "user_id": user_id
    }

    auth = AuthService(getattr(request, 'uow', None))
    result = auth.signup_user(request_dto)

    if result.is_success:
        result = Result.ok({"user_id": user_id})

    return present_result(result)


@api_bp.route("/auth/login", methods=["POST"])
@atomic
def login_user():
    request_dto = {
        **request.get_json()
    }

    auth = AuthService(getattr(request, 'uow', None))
    result = auth.login_user(request_dto)

    if result.is_success:
        result = Result.ok({"token": result.value})

    return present_result(result)


@api_bp.route("/federation/team/create_team", methods=["POST"])
@atomic
def create_team():
    team_id = str(uuid4())
    request_dto = {
        **request.get_json(),
        "team_id": team_id
    }
    federation = VolleyballFederationService(getattr(request, 'uow', None))
    result = federation.new_team(request_dto)

    if result.is_success:
        result = Result.ok({"team_id": team_id})

    return present_result(result)


@api_bp.route("/federation/stadium/build_stadium", methods=["POST"])
@atomic
def build_stadium():
    stadium_id = str(uuid4())
    request_dto = {
        **request.get_json(),
        "stadium_id": stadium_id
    }
    federation = VolleyballFederationService(getattr(request, 'uow', None))
    result = federation.build_stadium(request_dto)

    if result.is_success:
        result = Result.ok({"stadium_id": stadium_id})

    return present_result(result)


@api_bp.route("/federation/match/new_match", methods=["POST"])
@atomic
def new_match():
    match_id = str(uuid4())
    request_dto = {
        **request.get_json(),
        "match_id": match_id
    }
    federation = VolleyballFederationService(getattr(request, 'uow', None))
    result = federation.new_match(request_dto)

    if result.is_success:
        result = Result.ok({"match_id": match_id})

    return present_result(result)


@api_bp.route("/federation/match/define_match_seats", methods=["PUT"])
@atomic
def define_seats_for_match():
    request_dto = {
        **request.get_json()
    }
    federation = VolleyballFederationService(getattr(request, 'uow', None))
    result = federation.define_seats_for_match(request_dto)

    return present_result(result)
