import os
from operator import itemgetter
from typing import Any, Dict, List, Tuple

from fastapi import HTTPException, Request
from langchain_community.chat_models import ChatOpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores.pgvector import PGVector
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    format_document,
)
from langchain_core.prompts.prompt import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.runnables import (
    ConfigurableFieldSpec,
    RunnableBranch,
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
)
from langchain_core.runnables.config import RunnableConfig
from langchain_core.runnables.history import RunnableWithMessageHistory
# from langfuse.callback import CallbackHandler
from typing_extensions import TypedDict

from app.sql_history import SqlMessageHistory
from dotenv import load_dotenv
from app.config import PG_COLLECTION_NAME

load_dotenv()

vector_store = PGVector(
    collection_name=PG_COLLECTION_NAME,
    connection_string=os.getenv("POSTGRES_CONNECTION_STRING"),
    embedding_function=OpenAIEmbeddings(),
)

retriever = vector_store.as_retriever()

# RAG answer synthesis prompt
template = """You are a helpful website navigator. When the user asks how to perform a specific action you help them navigate to the specific application and also the steps to take in that application. Only give the answer in below format.

Example:
User: How do I request time off?
You: To request time off, navigate to Station-H -> Resource -> Apps -> People Process -> D HR -> Time Off -> Request Time Off

Here is some context:
<context>
{context}
</context>"""
ANSWER_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", template),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
    ]
)

# Conversational Retrieval Chain
DEFAULT_DOCUMENT_PROMPT = PromptTemplate.from_template(
    template="{page_content}, navigation path:{navigation_path}"
)


def _combine_documents(
    docs, document_prompt=DEFAULT_DOCUMENT_PROMPT, document_separator="\n\n"
):
    doc_strings = [format_document(doc, document_prompt) for doc in docs]

    print(doc_strings)
    return document_separator.join(doc_strings)


def _per_request_config_modifier(
    config: Dict[str, Any], request: Request
) -> Dict[str, Any]:
    """Update the config"""
    config = config.copy()
    configurable = config.get("configurable", {})

    # modify config for langfuse tracing

    # langfuse_handler = CallbackHandler(
    #     user_id=configurable["user_id"], session_id=configurable["conversation_id"]
    # )

    # config = RunnableConfig(
    #     callbacks=[langfuse_handler],
    # )

    config["configurable"] = configurable

    return config


store = {}


def get_session_history(user_id: str, conversation_id: str) -> BaseChatMessageHistory:
    if (user_id, conversation_id) not in store:
        store[(user_id, conversation_id)] = SqlMessageHistory(
            conversation_id=conversation_id
        )
    return store[(user_id, conversation_id)]

_inputs = RunnableParallel(
    {
        "input": lambda x: x["input"],
        "chat_history": lambda x: (x["chat_history"]),
        "context": RunnableLambda(itemgetter("input")) | retriever | _combine_documents,
    }
)

chain = _inputs | ANSWER_PROMPT | ChatOpenAI(model='gpt-4o') | StrOutputParser()


class ChatInput(TypedDict):
    input: str


chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history=get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
    history_factory_config=[
        ConfigurableFieldSpec(
            id="user_id",
            annotation=str,
            name="User ID",
            description="Unique identifier for the user.",
            default="",
            is_shared=True,
        ),
        ConfigurableFieldSpec(
            id="conversation_id",
            annotation=str,
            name="Conversation ID",
            description="Unique identifier for the conversation.",
            default="",
            is_shared=True,
        ),
    ],
).with_types(input_type=ChatInput)
