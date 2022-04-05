from fastapi import APIRouter, File, UploadFile, Form
from app.models.database import Database
from app.schemas.schema import StructureDocument, StructureCreateDocument
from dotenv import load_dotenv
from app.models.analyze import Analyze
import os

load_dotenv()
URI = os.getenv('URI')

router = APIRouter()
db = Database(URI)
analyze = Analyze()


@router.get('/api/specifications')
def get_specifications():
    return db.get_specifications()


@router.get('/api/specifications/full')
def get_specifications():
    return db.get_specifications_full()


@router.get('/api/specifications/{specification_id}')
def get_specification(specification_id: str):
    return db.get_specification(specification_id)


@router.put('/api/specifications/{specification_id}')
def update_specification(specification_id: str, doc_structure: StructureDocument):
    return db.update_specification(specification_id, doc_structure)


@router.post('/api/specifications')
def create_document(data: StructureCreateDocument):
    return db.create_document(data)


@router.get('/api/specifications/{specification_id}/keywords')
def get_keywords_by_specification_id(specification_id: str, mode: str):
    """
    :param specification_id: parsed document id from MongoDB collection
    :param mode: mode takes next variants: tf_idf, pullenti, combine
    """
    specifications_mongo = db.get_specifications_mongo()
    specification_current = db.get_specification(specification_id)
    doc_name = specification_current.documentName

    return analyze.get_keywords_by_specification_id(specifications_mongo, doc_name, mode)


@router.get('/api/templates/{template_id}')
def get_template(template_id: str):
    return db.get_template(template_id)


@router.post('/api/file')
async def parse_upload_file(filename: str = Form(...), file: UploadFile = File(...)):
    return await db.parse_doc_by_template(filename, file)
