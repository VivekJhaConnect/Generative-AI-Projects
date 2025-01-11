# Importing the required libraries
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings


def load_pdf_file(data):
    """
    Load the PDF file and return the text data
    """
    loader = DirectoryLoader(
        data,
        glob="*.pdf",
        loader_cls=PyPDFLoader
    )
    
    documents = loader.load()

    return documents

# Split the Data into Text Chunks

def split_text(data):
    """
    Split the text data into chunks
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
    text_chunks = text_splitter.split_documents(data)
    return text_chunks

# Download the embeddings from the Hugging Face Model Hub
def download_hugging_face_embeddings():
    """
    Download the embeddings from the Hugging Face Model Hub
    """
    
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return embeddings