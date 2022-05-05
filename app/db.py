import databases
import ormar
import sqlalchemy

from .config import settings

database = databases.Database(settings.db_url)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class Questions(ormar.Model):
    class Meta(BaseMeta):
        tablename = "questions"

    id: int = ormar.Integer(primary_key=True, autoincrement=False)
    question: str = ormar.String(max_length=256, unique=False, nullable=False)
    answer: str = ormar.String(max_length=256, unique=False, nullable=False)
    created_at: str = ormar.DateTime(unique=False, nullable=False)

engine = sqlalchemy.create_engine(settings.db_url)
metadata.create_all(engine)