import os

from databases import Database
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    MetaData,
    String,
    Table,
    Text,
    create_engine,
    func,
)

DATABASE_URL = os.getenv("DATABASE_URL")

database = Database(DATABASE_URL)
metadata = MetaData()

contact_messages = Table(
    "contact_messages",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(255)),
    Column("email", String(255)),
    Column("message", Text),
    Column("created_at", DateTime, server_default=func.now()),
)

engine = create_engine(DATABASE_URL)
metadata.create_all(engine)
