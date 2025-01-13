from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from src.prompt import *
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=r"C:\Users\ADMIN\Documents\venv\.env")
os.environ['PINECONE_API_KEY']=os.getenv("PINECONE_API_KEY")
os.environ['OPENAI_API_KEY']=os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

embeddings = download_hugging_face_embeddings()

index_name = "medical-chatbot"

# Embed each chunk and upset the embedding into your Pinecone index.
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings,
)

retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})

llm = OpenAI(temperature=0.4, max_tokens=500)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),  # Corrected: changed "System" -> "system"
        ("user", "{input}"),        # Changed role to "user"
    ]
)

question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

@app.route("/")
def index():
    return render_template("chat.html")

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    print(input)
    response = rag_chain.invoke({'input': msg})
    print('response: ', response['answer'])
    return str(response['answer'])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)