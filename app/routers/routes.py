from fastapi import APIRouter, File, UploadFile
from typing import Optional, Dict
from app.schemas.schema import StructureDocument, StructureCreateDocument
from app import db, analyze


router = APIRouter()


@router.post('/api/specification/', tags=["specifications"])
def create_document(data: StructureCreateDocument):
    return db.create_document(data)


@router.get('/api/specification/', tags=["specifications"])
def get_specifications(full: bool = False):
    if not full:
        return db.get_specifications()
    return db.get_specifications_full()


@router.get('/api/specification/{specification_id}', tags=["specifications"])
def get_specification(specification_id: str):
    return db.get_specification(specification_id)


@router.put('/api/specification/{specification_id}', tags=["specifications"])
def update_specification(specification_id: str, doc_structure: StructureDocument):
    return db.update_specification(specification_id, doc_structure)


@router.get('/api/specification/{specification_id}/keywords', tags=["specifications"])
def get_keywords_by_specification_id(specification_id: str, mode: str, section: Optional[str] = None):
    specifications_mongo = db.get_specifications_mongo()
    specification_current = db.get_specification(specification_id)
    doc_name = specification_current.documentName

    return analyze.get_keywords_by_specification_id(specifications_mongo, doc_name, mode, section)


@router.post('/api/template/', tags=["templates"])
def create_document(data: StructureCreateDocument):
    return db.create_template(data)


@router.get('/api/template/', tags=["templates"])
def get_templates():
    return db.get_templates()


@router.get('/api/template/{template_id}', tags=["templates"])
def get_template(template_id: str):
    return db.get_template(template_id)


@router.post('/api/file/')
async def parse_file(file: UploadFile = File(...)):
    return await db.parse_doc_by_template(file)


@router.get('/api/section/{document_id}')
def get_sections(document_id: str):
    document_structure: Dict = db.get_specification(document_id).structure[0]

    return analyze.get_sections(document_structure)
