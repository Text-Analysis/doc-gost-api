from enum import Enum
from typing import List, Dict, Optional

from pydantic import BaseModel


class Entity(BaseModel):
    id: str
    name: str


class Document(Entity):
    templateId: str
    structure: List
    keywords: Optional[List] = None


class Template(Entity):
    structure: List


class DocumentUpdate(BaseModel):
    structure: Optional[List] = None
    keywords: Optional[List] = None


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
