from fastapi import APIRouter, File, UploadFile
from typing import Optional, Dict
from app.schemas.schema import StructureDocument, StructureCreateDocument
from app import db, analyze


router = APIRouter()


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
def get_keywords_by_specification_id(specification_id: str, mode: str, section: Optional[str] = None):
    specifications_mongo = db.get_specifications_mongo()
    specification_current = db.get_specification(specification_id)
    doc_name = specification_current.documentName

    return analyze.get_keywords_by_specification_id(specifications_mongo, doc_name, mode, section)


@router.get('/api/templates')
def get_templates():
    return db.get_templates()


@router.get('/api/templates/{template_id}')
def get_template(template_id: str):
    return db.get_template(template_id)


@router.post('/api/file')
async def parse_file(file: UploadFile = File(...)):
    return await db.parse_doc_by_template(file)


@router.get('/api/sections/{document_id}')
def get_sections(document_id: str):
    document_structure: Dict = db.get_specification(document_id).structure[0]

    return analyze.get_sections(document_structure)
