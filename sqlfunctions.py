import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import BigInteger, Column, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import Engine
from sqlalchemy.inspection import inspect
import datetime



Base = declarative_base()

class UserInteraction(Base):
    __tablename__ = 'user_interactions'

    Id = Column(BigInteger, primary_key=True, unique=True, nullable=False)
    PrimaryBotOveride = Column(Boolean)
    SelectedOption = Column(String)
    ChatId = Column(String)
    CreationTime = Column(DateTime, default=datetime.datetime.now)

def create_user_interaction_table(engine: Engine):
    # Create a session
    SessionClass = sessionmaker(bind=engine)
    session = SessionClass()

    # Check if the table already exists
    inspector = inspect(engine)
    if not inspector.has_table(UserInteraction.__tablename__):
        # If the table does not exist, create it
        Base.metadata.create_all(engine)
        print(f"Table '{UserInteraction.__tablename__}' has been created.")
    else:
        print(f"Table '{UserInteraction.__tablename__}' already exists.")

    # Close the session
    session.close()


