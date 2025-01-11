from src.helper import load_pdf_file, split_text, download_hugging_face_embeddings
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=r"C:\Users\ADMIN\Documents\venv\.env")
os.environ['PINECONE_API_KEY']=os.getenv("PINECONE_API_KEY")
os.environ['OPENAI_API_KEY']=os.getenv("OPENAI_API_KEY")

extracted_data = load_pdf_file(data="Data/")
text_chunk = split_text(extracted_data)
embeddings = download_hugging_face_embeddings()


pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

index_name = "medical-chatbot"

pc.create_index(
    name=index_name,
    dimension=384, # Replace with your model dimensions
    metric="cosine", # Replace with your model metric
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    ) 
)

# Embed each chunk and upset the embedding into your Pinecone index.
docsearch = PineconeVectorStore.from_documents(
    documents=text_chunk,
    index_name=index_name,
    embedding=embeddings,
)
