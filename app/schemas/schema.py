from pydantic import BaseModel
from typing import List, Optional
from enum import Enum


class Entity(BaseModel):
    id: str
    name: str


class Document(Entity):
    template_id: Optional[str] = None
    structure: List


class Template(Entity):
    structure: List


class StructureDocument(BaseModel):
    structure: List


class DocumentCreateStructure(BaseModel):
    name: str
    template_id: str
    structure: List


class TemplateCreateStructure(BaseModel):
    name: str
    structure: List


class KeywordExtractionMode(str, Enum):
    pullenti = 'pullenti'
    tf_idf = 'tf_idf'
    combine = 'combine'
