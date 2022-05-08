from pydantic import BaseModel
from typing import List, Dict
from enum import Enum


class Entity(BaseModel):
    id: str
    name: str


class Document(Entity):
    templateId: str
    structure: List


class Template(Entity):
    structure: List


class StructureDocument(BaseModel):
    structure: List


class DocumentCreateStructure(BaseModel):
    name: str
    templateId: str
    structure: List


class TemplateCreateStructure(BaseModel):
    name: str
    structure: Dict


class KeywordExtractionMode(str, Enum):
    pullenti = 'pullenti'
    tf_idf = 'tf_idf'
    combine = 'combine'
