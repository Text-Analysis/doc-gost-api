from pydantic import BaseModel
from typing import List


class DocumentShort(BaseModel):
    id: str
    name: str


class Document(BaseModel):
    id: str
    name: str
    structure: List


class StructureDocument(BaseModel):
    structure: List


class StructureCreateDocument(BaseModel):
    name: str
    structure: List
