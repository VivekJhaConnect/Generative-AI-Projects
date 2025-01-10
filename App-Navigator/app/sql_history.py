import json
from pydantic import BaseModel
from langchain.schema import BaseChatMessageHistory
from sqlmodel import Session
from langchain.schema.messages import (
    AIMessageChunk,
    AIMessage,
    HumanMessage,
    SystemMessage,
)

from . import database
from . import models


def get_messages_by_conversation_id(
    conversation_id: str,
) -> AIMessageChunk | HumanMessage | SystemMessage | AIMessage:
    """
    Finds all messages that belong to the given conversation_id

    :param conversation_id: The id of the conversation

    :return: A list of messages
    """

    with Session(database.engine) as session:
        messages = session.query(models.Message).filter_by(
            conversation_id=conversation_id
        )

        return [message.as_lc_message() for message in messages]


def add_message_to_conversation(
    conversation_id: str, role: str, content: str
) -> models.Message:
    """
    Creates and stores a new message tied to the given conversation_id
        with the provided role and content

    :param conversation_id: The id of the conversation
    :param role: The role of the message
    :param content: The content of the message

    :return: The created message
    """
    with Session(database.engine) as session:
        message = models.Message(
            conversation_id=conversation_id, role=role, content=content
        )
        # session.add(message)
        # session.commit()
        # session.refresh(message)

        return message


class SqlMessageHistory(BaseChatMessageHistory, BaseModel):
    conversation_id: str

    @property
    def messages(self):
        return get_messages_by_conversation_id(self.conversation_id)

    def add_message(self, message):

        return add_message_to_conversation(
            conversation_id=self.conversation_id,
            role=message.type,
            content=message.content,
        )

    def clear(self):
        pass
