from database import SqlAlchemyORM


def init_db():
    orm = SqlAlchemyORM()
    orm.configure_mapper()
    orm.create_schema()
    orm.create_tables()


if __name__ == '__main__':
    init_db()
