from typing import Optional, Dict

from fastapi import APIRouter, File, UploadFile, Form
from fastapi.responses import FileResponse

from app.config import db, parser
from app.errors.errors import UnprocessableDataException, ResourceNotFoundException
from app.schemas.schema import DocumentCreateStructure, \
    Document, KeywordExtractionMode, TemplateCreateStructure, DocumentUpdate
from .error import RouteErrorHandle

router = APIRouter(route_class=RouteErrorHandle)


@router.post('/documents', tags=['documents'])
def create_document(data: DocumentCreateStructure):
    created = db.create_document(data)
    if not created:
        raise UnprocessableDataException('input data is not valid')
    return 'ok'


@router.get('/documents', tags=['documents'])
def get_documents(short: bool = True):
    if short:
        return db.get_documents_short()
    return db.get_documents()


@router.get('/documents/{document_id}', tags=['documents'])
def get_document(document_id: str):
    document = db.get_document(document_id)
    if not document:
        raise ResourceNotFoundException(f'document with object_id={document_id} not found')
    return document


@router.patch('/documents/{document_id}', tags=['documents'])
def update_document(document_id: str, model: DocumentUpdate):
    document = db.get_document(document_id)
    if not document:
        raise ResourceNotFoundException(f'document with object_id={document_id} not found')
    update_data = model.dict(exclude_unset=True)
    if "structure" in update_data:
        return db.update_document_structure(document_id, update_data["structure"])
    if "keywords" in update_data:
        return db.update_document_keywords(document_id, update_data["keywords"])
    raise UnprocessableDataException('data is null')


@router.delete('/documents/{document_id}', tags=['documents'])
def delete_document(document_id: str):
    document = db.get_document(document_id)
    if not document:
        raise ResourceNotFoundException(f'document with object_id={document_id} not found')
    return db.delete_document(document_id)


@router.get('/documents/{document_id}/keywords', tags=['documents'])
def get_document_keywords(document_id: str):
    document = db.get_document(document_id)
    if not document:
        raise ResourceNotFoundException(f'document with object_id={document_id} not found')
    return db.get_document_keywords(document_id)


@router.get('/documents/{document_id}/keywords/generation', tags=['documents'])
def generation_document_keywords(document_id: str, mode: KeywordExtractionMode, section_name: Optional[str] = None):
    documents = db.get_mongo_documents()
    document = Document(id='', name='', templateId='', structure=[])
    for d in documents:
        if str(d.get('_id')) == document_id:
            document.id = str(d.get('_id'))
            document.name = d.get('name')
            document.templateId = d.get('templateId')
            document.structure = [d.get('section_tree')]
            break
    if not document.id:
        raise ResourceNotFoundException(f'document with object_id={document_id} not found')
    if mode == KeywordExtractionMode.tf_idf:
        return parser.extract_tf_idf_pairs(documents, document.name, section_name)
    if mode == KeywordExtractionMode.pullenti:
        return parser.extract_keywords(documents, document.name, section_name)
    if mode == KeywordExtractionMode.combine:
        return parser.extract_rationized_keywords(documents, document.name, section_name)
    raise UnprocessableDataException(f'keyword extraction mode {mode} is not valid')


@router.get('/documents/{document_id}/download', tags=['documents'])
def download_document(document_id: str):
    document = db.get_document(document_id)
    if not document:
        raise ResourceNotFoundException(f'document with object_id={document_id} not found')
    file_path = parser.save_document_as_docx(document.name, document.structure[0])
    parser.clean_document(file_path)
    return FileResponse(path=file_path, filename=file_path)


@router.get('/documents/{document_id}/sections', tags=['documents'])
def get_sections(document_id: str):
    document = db.get_document(document_id)
    if not document:
        raise ResourceNotFoundException(f'document with object_id={document_id} not found')
    document_structure: Dict = document.structure[0]
    return parser.get_section_names(document_structure)


@router.post('/templates', tags=['templates'])
def create_template(data: TemplateCreateStructure):
    created = db.create_template(data)
    if not created:
        raise UnprocessableDataException('input data is not valid')
    return 'ok'


@router.get('/templates', tags=['templates'])
def get_templates():
    return db.get_templates_short()


@router.get('/templates/{template_id}', tags=['templates'])
def get_template(template_id: str):
    template = db.get_template(template_id)
    if not template:
        raise ResourceNotFoundException(f'template with object_id={template_id} not found')
    return template


@router.delete('/templates/{template_id}', tags=['templates'])
def delete_template(template_id: str):
    template = db.get_template(template_id)
    if not template:
        raise ResourceNotFoundException(f'template with object_id={template_id} not found')
    return db.delete_template(template_id)


@router.post('/files', tags=['other'])
async def parse_file(file: UploadFile = File(...), template_id: str = Form(...)):
    template = db.get_template(template_id)
    if not template:
        raise ResourceNotFoundException(f'template with object_id={template_id} not found')
    return await db.parse_docx_by_template(template, file)


@router.put('/db', tags=['other'])
def change_connect_database(mongodb_connstring: str):
    db.change_connect_database(mongodb_connstring)
    return 'ok'
