from fastapi import APIRouter, File, UploadFile
from app.models.database import Database
from app.schemas.schema import StructureDocument, StructureCreateDocument
from dotenv import load_dotenv
import os

load_dotenv()
URI = os.getenv('URI')

router = APIRouter()
db = Database(URI)


@router.get('/api/specifications')
def get_specifications():
    return db.get_specifications()


@router.get('/api/specifications/{specification_id}')
def get_specification(specification_id: str):
    return db.get_specification(specification_id)


@router.put('/api/specifications/{specification_id}')
def update_specification(specification_id: str, doc_structure: StructureDocument):
    return db.update_specification(specification_id, doc_structure)


@router.post('/api/specifications')
def create_document(data: StructureCreateDocument):
    return db.create_document(data)


@router.get('/api/templates/{template_id}')
def get_template(template_id: str):
    return db.get_template(template_id)


@router.post('/api/file')
async def parse_upload_file(file: UploadFile = File(...)):
    return await db.parse_doc_by_template(file)
