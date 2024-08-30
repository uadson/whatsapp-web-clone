import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, create_engine, Session, select


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    password: str
    
    
class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    receiver_id: int
    message: str
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


def init_db():
    engine = create_engine("sqlite:///.test.db")
    SQLModel.metadata.create_all(engine)