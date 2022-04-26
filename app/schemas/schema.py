from pydantic import BaseModel
from typing import List


class Document(BaseModel):
    id: str
    name: str


class DocumentFull(BaseModel):
    id: str
    name: str
    structure: List


class StructureDocument(BaseModel):
    structure: List


class StructureCreateDocument(BaseModel):
    name: str
    structure: List
