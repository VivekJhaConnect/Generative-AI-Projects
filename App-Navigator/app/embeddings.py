import os

from langchain_community.document_loaders import PyPDFLoader, UnstructuredHTMLLoader
from langchain_community.vectorstores.pgvector import PGVector
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

from app.config import EMBEDDING_MODEL, PG_COLLECTION_NAME

from dotenv import load_dotenv

load_dotenv()


def create_embeddings(file_path: str, nav_path: str = ''):
    # Initialize embeddings and text splitter
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)

    # Load the html document using a custom loader for a single file

    loader = UnstructuredHTMLLoader(file_path)
    chunks = loader.load_and_split(text_splitter)

    navigation_path = nav_path

    # set naviation_path metadata for each chunk
    for chunk in chunks:
        chunk.metadata["navigation_path"] = navigation_path

    # Store the document chunks embeddings in PGVector
    PGVector.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=PG_COLLECTION_NAME,
        connection_string=os.getenv("POSTGRES_CONNECTION_STRING"),
        pre_delete_collection=False,
    )


# Example usage
if __name__ == "__main__":
    file_path = ""  # This should be replaced with the actual file path
    create_embeddings(file_path)
