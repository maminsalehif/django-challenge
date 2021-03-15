from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, ARRAY
from sqlalchemy.ext.declarative import declarative_base

from database.mutable_array import MutableList
from auth.entity import User, UserCredential
from shared.valueobject import UserID, StadiumID, SeatID, TeamID, MatchID
from volleyball_federation.entity import Stadium, Seat, Team, Match

Base = declarative_base()


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, unique=True)
    role = Column(String)
    fullname = Column(String)
    phone_number = Column(String)

    def to_entity(self) -> User:
        return User(
            user_id=UserID(self.user_id),
            fullname=self.fullname,
            phone_number=self.phone_number,
        )

    @staticmethod
    def from_entity(user: User) -> 'UserModel':
        return UserModel(
            user_id=user.user_id.id_,
            role='USER',
            fullname=user.fullname,
            phone_number=user.phone_number
        )


class UserCredentialModel(Base):
    __tablename__ = "users_credential"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, unique=True)
    phone_number = Column(String)
    password = Column(String)

    def to_entity(self) -> UserCredential:
        return UserCredential(
            user_id=UserID(self.user_id),
            phone_number=self.phone_number,
            hashed_password=self.password
        )

    @staticmethod
    def from_entity(user_credential: UserCredential) -> 'UserCredentialModel':
        return UserCredentialModel(
            user_id=user_credential.user_id.id_,
            phone_number=user_credential.phone_number,
            password=user_credential.hashed_password
        )


class StadiumModel(Base):
    __tablename__ = "stadiums"

    id = Column(Integer, primary_key=True)
    stadium_id = Column(String, unique=True)
    name = Column(String)
    seats = Column(MutableList.as_mutable(ARRAY(String)))

    def to_entity(self) -> Stadium:
        return Stadium(
            stadium_id=StadiumID(self.stadium_id),
            name=self.name,
            seats=list(map(lambda seat_id: Seat(seat_id=SeatID(seat_id)), self.seats))
        )

    @staticmethod
    def from_entity(stadium: Stadium) -> 'StadiumModel':
        return StadiumModel(
            stadium_id=stadium.stadium_id.id_,
            name=stadium.name,
            seats=list(map(lambda seat: seat.seat_id.id_, stadium.seats))
        )


class TeamModel(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True)
    team_id = Column(String, unique=True)
    name = Column(String)

    def to_entity(self) -> Team:
        return Team(
            team_id=TeamID(self.team_id),
            name=self.name
        )

    @staticmethod
    def from_entity(team: Team) -> 'TeamModel':
        return TeamModel(
            team_id=team.team_id.id_,
            name=team.name
        )


class MatchModel(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True)
    match_id = Column(String, unique=True)
    host_team_id = Column(String)
    guest_team_id = Column(String)
    stadium_id = Column(String)
    stadium_seats = Column(MutableList.as_mutable(ARRAY(String)))
    time = Column(Float)

    def to_entity(self) -> Match:
        return Match(
            match_id=MatchID(self.match_id),
            host_team_id=TeamID(self.host_team_id),
            guest_team_id=TeamID(self.guest_team_id),
            stadium_id=StadiumID(self.stadium_id),
            time=datetime.fromtimestamp(self.time),
            stadium_seats=list(map(SeatID, self.stadium_seats))
        )

    @staticmethod
    def from_entity(match: Match) -> 'MatchModel':
        return MatchModel(
            match_id=match.match_id.id_,
            host_team_id=match.host_team_id.id_,
            guest_team_id=match.guest_team_id.id_,
            stadium_id=match.stadium_id.id_,
            time=match.time.timestamp(),
            stadium_seats=list(map(lambda seat_id: seat_id.id_, match.stadium_seats))
        )
