from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import config, Structure
from bson.objectid import ObjectId

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

coll = config('techSpecifications')


@app.get('/api/specifications')
def get_specifications():
    data = []
    for value in coll.find({}, {'document_name': 1}):
        data.append({
            'id': str(value.get('_id')),
            'documentName': value.get('document_name')
        })
    return {'data': data}


@app.get('/api/specifications/{specification_id}')
def get_specification(specification_id: str):
    specification = coll.find_one({'_id': ObjectId(specification_id)})
    return {
        'id': str(specification.get('_id')),
        'documentName': specification.get('document_name'),
        'structure': [specification.get('structure')]
    }


@app.put('/api/specifications/{specification_id}')
def update_specification(specification_id: str, doc_structure: Structure):
    current = {'_id': ObjectId(specification_id)}
    new_data = {'$set': {'structure': doc_structure.structure[0]}}
    coll.update_one(current, new_data)
    return 'Ok'
