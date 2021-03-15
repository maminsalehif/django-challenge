import importlib
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy_utils import create_database

from database.unit_of_work import AlchemyUnitOfWork


class SqlAlchemyORM:
    def __init__(self):
        self.engine = create_engine(
            f"postgresql://"
            f"{os.getenv('POSTGRES_USER', 'postgres')}:{os.getenv('POSTGRES_PASSWORD', '123')}"
            f"@{os.getenv('POSTGRES_HOST', '185.235.41.175:5432')}/{os.getenv('POSTGRES_DBNAME', 'postgres')}"
        )
        self.session_maker = lambda: scoped_session(sessionmaker(self.engine))
        self.base = None

    def create_schema(self):
        create_database(self.engine.url)

    def create_tables(self):
        self.configure_mapper()
        self.base.metadata.create_all(self.engine)

    def configure_mapper(self):
        models = importlib.import_module(".models", __package__)
        self.base = models.Base

    def unit_of_work(self) -> AlchemyUnitOfWork:
        return AlchemyUnitOfWork(self.session_maker)
