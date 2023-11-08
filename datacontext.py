import random
from sqlalchemy import BigInteger, create_engine, Column, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import datetime

from sqlfunctions import create_user_interaction_table

Base = declarative_base()
def generate_random_float(min_value, max_value):
    return random.uniform(min_value, max_value)

class UserInteraction(Base):
    __tablename__ = 'user_interactions'
    Id = Column(BigInteger, primary_key=True, unique=True, nullable=False)
    PrimaryBotOveride = Column(Boolean)
    SelectedOption = Column(String)
    ChatId = Column(String)
    CreationTime = Column(DateTime, default=datetime.datetime.now)


def SaveUserInteraction(payload):
    connection_string = "mssql+pyodbc://NANOTECH\SQLEXPRESS/ChatBot?driver=ODBC+Driver+17+for+SQL+Server"
    engine = create_engine(connection_string)
    create_user_interaction_table(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    chat_id_to_check = payload["chatId"]

    # Check if a user interaction with the same 'chatId' exists
    existing_interaction = session.query(UserInteraction).filter(UserInteraction.ChatId == chat_id_to_check).first()

    if existing_interaction:
        # If an interaction with the same 'chatId' exists, update its attributes
        existing_interaction.PrimaryBotOveride = payload["Override"]
        existing_interaction.SelectedOption = payload["Option"]
        existing_interaction.CreationTime = datetime.datetime.now()
    else:
        # If it doesn't exist, create a new interaction
        new_interaction = UserInteraction(
            PrimaryBotOveride=payload["Override"],
            SelectedOption=payload["Option"],
            ChatId=payload["chatId"],
            CreationTime=datetime.datetime.now()
        )

        session.add(new_interaction)

    session.commit()
    session.close()
