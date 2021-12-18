from pymongo import MongoClient
from pydantic import BaseModel
from typing import List


def config():

    client = MongoClient('')
    db = client.documentsAnalysis

    return db


class StructureDocument(BaseModel):
    structure: List


class StructureCreateDocument(BaseModel):
    name: str
    structure: List
