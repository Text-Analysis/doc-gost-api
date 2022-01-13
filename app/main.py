from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import Database
from app.models import StructureDocument, StructureCreateDocument
from dotenv import load_dotenv
import os

load_dotenv()

URI = os.getenv('URI')

app = FastAPI()
db = Database(URI)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/api/specifications')
def get_specifications():

    return db.get_specifications()


@app.get('/api/specifications/{specification_id}')
def get_specification(specification_id: str):

    return db.get_specification(specification_id)


@app.put('/api/specifications/{specification_id}')
def update_specification(specification_id: str, doc_structure: StructureDocument):

    return db.update_specification(specification_id, doc_structure)


@app.post('/api/specifications')
def create_document(data: StructureCreateDocument):
    return db.create_document(data)


@app.get('/api/templates/{template_id}')
def get_template(template_id: str):

    return db.get_template(template_id)
