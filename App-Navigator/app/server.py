import os
from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes
from pydantic import BaseModel
from sqlmodel import Session, select
from app.embeddings import create_embeddings
from app.database import engine, create_db_and_tables
from app.models import Conversation
# from app.agent import agent_with_history

from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
# from app.image_gen import chain
from dotenv import load_dotenv
# from langfuse.callback import CallbackHandler
from app.chain import chain_with_history, _per_request_config_modifier


load_dotenv()

app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="Spin up a simple api server using Langchain's Runnable interfaces",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    nav_path: str

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/files/upload", tags=["files"])
async def upload_file(file: UploadFile, nav_path: str = Form(...)):

    file_path = f"uploads/{file.filename}"
    print(nav_path)
    # if uploads path does not exist, create it
    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    # save file to disk
    with open(file_path, "wb") as f:
        f.write(file.file.read())

        create_embeddings(file_path, nav_path)

    return {"filename": file.filename, "message": "File uploaded successfully"}


add_routes(
    app, chain_with_history, per_req_config_modifier=_per_request_config_modifier
)
