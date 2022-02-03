from pydantic import BaseModel
from typing import List


class Specification(BaseModel):
    id: str
    documentName: str


class SpecificationFull(BaseModel):
    id: str
    documentName: str
    structure: List


class StructureDocument(BaseModel):
    structure: List


class StructureCreateDocument(BaseModel):
    name: str
    structure: List
