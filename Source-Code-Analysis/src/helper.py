
from git import Repo
from langchain.text_splitter import Language
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import LanguageParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationSummaryMemory
from langchain.chains import ConversationalRetrievalChain


# Clone any github repository
def repo_ingestion(repo_url):
    os.makedirs('repo', exist_ok=True)
    repo_path = "repo/"
    Repo.clone_from(repo_url, to_path=repo_path)

# Loading repository as documents
def load_repo(repo_path):
    loader = GenericLoader.from_filesystem(repo_path,
                                       glob="**/*",
                                       suffixes=[".ipynb", ".py"],
                                       parser=LanguageParser(language=Language.PYTHON, parser_threshold=0.5))
        
    documents = loader.load()
    return documents

# Creating test chunks
def text_splitter(documents):
    documents_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON,
        chunk_size=300,
        chunk_overlap=20
    )
    text_chunks = documents_splitter.split_documents(documents)

    return text_chunks

# loading embeddings models
def load_embeddings():
    embeddings = OpenAIEmbeddings(disallowed_special=())
    return embeddings

