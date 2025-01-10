import uuid
from datetime import datetime
from typing import List, Optional, Union

from langchain.schema.messages import (
    AIMessageChunk,
    HumanMessage,
    SystemMessage,
    AIMessage,
)
from sqlmodel import Field, Relationship, SQLModel


class BaseModel(SQLModel):
    created_at: datetime = Field(default=datetime.now(), nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)


class Conversation(BaseModel, table=True):
    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
    )
    user_id: int = Field(default=None, nullable=False)
    # Relationships
    messages: List["Message"] = Relationship(back_populates="conversation")


class Message(BaseModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    role: str = Field(nullable=False)
    content: str = Field(nullable=False)

    conversation_id: str = Field(
        default=None, foreign_key="conversation.id", nullable=False
    )
    conversation: "Conversation" = Relationship(back_populates="messages")

    def as_dict(self):
        return {"id": self.id, "role": self.role, "content": self.content}

    def as_lc_message(self) -> Union[HumanMessage, AIMessageChunk, SystemMessage]:
        if self.role == "human":
            return HumanMessage(content=self.content)
        elif self.role == "AIMessageChunk":
            return AIMessageChunk(content=self.content)
        elif self.role == "ai":
            return AIMessage(content=self.content)
        elif self.role == "system":
            return SystemMessage(content=self.content)
        else:
            raise Exception(f"Unknown message role: {self.role}")
