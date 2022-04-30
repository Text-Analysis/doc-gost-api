from pydantic import BaseModel
from typing import List, Optional
from enum import Enum


class DocumentShort(BaseModel):
    id: str
    name: str


class Document(BaseModel):
    id: str
    name: str
    tempId: Optional[str] = None
    structure: List


class StructureDocument(BaseModel):
    structure: List


class StructureCreateDocument(BaseModel):
    name: str
    tempId: Optional[str] = None
    structure: List


class KeywordExtractionMode(str, Enum):
    pullenti = 'pullenti'
    tf_idf = 'tf_idf'
    combine = 'combine'
