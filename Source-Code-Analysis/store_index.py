from src.helper import repo_ingestion, load_repo, text_splitter, load_embeddings
from dotenv import load_dotenv
from langchain.vectorstores import Chroma
import os

load_dotenv(dotenv_path=r"C:\Users\ADMIN\Documents\venv\.env")
os.environ['PINECONE_API_KEY']=os.getenv("PINECONE_API_KEY")
os.environ['OPENAI_API_KEY']=os.getenv("OPENAI_API_KEY")

documents = load_repo("repo")
text_chunks = text_splitter(documents)
embeddings = load_embeddings()

vectordb = Chroma.from_documents(text_chunks, embedding=embeddings, persist_directory="./db")
vectordb.persist()