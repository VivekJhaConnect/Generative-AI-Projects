import os
from sqlmodel import SQLModel, create_engine, Session


postgres_url = os.getenv("POSTGRES_CONNECTION_STRING")

engine = create_engine(postgres_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
