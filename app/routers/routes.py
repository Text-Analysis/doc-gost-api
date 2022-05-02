from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from typing import Optional, Dict
from app.schemas.schema import StructureDocument, DocumentCreateStructure, \
    Document, KeywordExtractionMode, TemplateCreateStructure
from app import db, parser

router = APIRouter()


@router.post('/api/documents', tags=['documents'])
def create_document(data: DocumentCreateStructure):
    created = db.create_document(data)
    if not created:
        raise HTTPException(status_code=422, detail='input data is not valid')
    return 'OK'


@router.get('/api/documents', tags=['documents'])
def get_documents(short: bool = True):
    if short:
        return db.get_documents_short()
    return db.get_documents()


@router.get('/api/documents/{document_id}', tags=['documents'])
def get_document(document_id: str):
    document = db.get_document(document_id)
    if not document:
        raise HTTPException(status_code=404, detail=f'document with _id={document_id} not found')
    return document


@router.put('/api/documents/{document_id}', tags=['documents'])
def update_document(document_id: str, document_structure: StructureDocument):
    document = db.get_document(document_id)
    if not document:
        raise HTTPException(status_code=404, detail=f'document with _id={document_id} not found')
    return db.update_document(document_id, document_structure)


@router.get('/api/documents/{document_id}/keywords', tags=['documents'])
def get_document_keywords(document_id: str, mode: KeywordExtractionMode, section_name: Optional[str] = None):
    documents = db.get_mongo_documents()

    document = Document(id='', name='', structure=[])
    for d in documents:
        if str(d.get('_id')) == document_id:
            document.id = str(d.get('_id'))
            document.name = d.get('name')
            document.structure = [d.get('section_tree')]
            break

    if not document.id:
        raise HTTPException(status_code=404, detail=f'document with _id={document_id} not found')

    if mode == KeywordExtractionMode.tf_idf:
        return parser.extract_tf_idf_pairs(documents, document.name, section_name)

    if mode == KeywordExtractionMode.pullenti:
        return parser.extract_keywords(documents, document.name, section_name)

    if mode == KeywordExtractionMode.combine:
        return parser.extract_rationized_keywords(documents, document.name, section_name)

    raise HTTPException(status_code=404, detail=f'keyword extraction mode {mode} not found')


@router.post('/api/templates', tags=['templates'])
def create_template(data: TemplateCreateStructure):
    created = db.create_template(data)
    if not created:
        raise HTTPException(status_code=422, detail='input data is not valid')
    return 'OK'


@router.get('/api/templates', tags=['templates'])
def get_templates():
    return db.get_templates_short()


@router.get('/api/templates/{template_id}', tags=['templates'])
def get_template(template_id: str):
    template = db.get_template(template_id)
    if not template:
        raise HTTPException(status_code=404, detail=f'template with _id={template_id} not found')
    return template


@router.post('/api/files')
async def parse_file(file: UploadFile = File(...), template_id: str = Form(...)):
    template = db.get_template(template_id)
    if not template:
        raise HTTPException(status_code=404, detail=f'template with _id={template_id} not found')
    try:
        return await db.parse_docx_by_template(template, file)
    except Exception:
        raise HTTPException(status_code=422, detail='file is not valid')


@router.get('/api/sections/{document_id}')
def get_sections(document_id: str):
    document = db.get_document(document_id)
    if not document:
        raise HTTPException(status_code=404, detail=f'document with _id={document_id} not found')

    document_structure: Dict = document.structure[0]
    return parser.get_section_names(document_structure)
