import sqlalchemy as db
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from sqlalchemy import Column, Integer, String
from dotenv import load_dotenv
import os

Base = declarative_base()

load_dotenv()

engine = db.create_engine(os.getenv("DB_URL"), echo=False)

session = scoped_session(sessionmaker(bind=engine))


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    value = Column(String, nullable=True)
    category = Column(String)

    def __repr__(self):
        return f"<Todo(name={self.name}, category={self.category})>"


# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
