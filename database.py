import sqlalchemy as db
import sqlalchemy as db
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, Date, Float, DateTime, Time


Base = declarative_base()

engine = db.create_engine("sqlite:///todo.db", echo=True)

Session = sessionmaker(bind=engine)
session = Session()


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    value = Column(String)
    category = Column(String)

    def __repr__(self):
        return f"<Todo(name={self.name}, category={self.category})>"

# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)