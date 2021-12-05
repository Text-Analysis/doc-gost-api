from pymongo import MongoClient
from pydantic import BaseModel
from typing import List


def config(name_coll: str):

    client = MongoClient('')
    db = client.documentsAnalysis

    return db[name_coll]


class Structure(BaseModel):
    structure: List
