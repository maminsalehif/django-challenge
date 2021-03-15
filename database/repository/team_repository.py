from sqlalchemy.orm import Session

from database.abc import TeamRepositoryABC
from database.models import TeamModel
from shared.result import Result
from shared.valueobject import TeamID, DomainError
from volleyball_federation.entity import Team


class TeamRepository(TeamRepositoryABC):
    def __init__(self, session: Session):
        self.session = session

    def create_team(self, team: Team) -> Result:
        self.session.add(TeamModel.from_entity(team))
        return Result.ok()

    def get_team(self, team_id: TeamID) -> Result:
        model_or_none = self.session.query(TeamModel).filter_by(team_id=team_id.id_).one_or_none()
        if model_or_none is None:
            return Result.fail(DomainError("TeamNotFound", None))

        return Result.ok(model_or_none.to_entity())
