from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import config, StructureDocument, StructureCreateDocument
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

config = config()
collSpecifications = config['requirementsSpecifications']
collTemp = config['sectionTreeTemplates']


@app.get('/api/specifications')
def get_specifications():
    data = []
    for value in collSpecifications.find({}, {'document_name': 1}):
        data.append({
            'id': str(value.get('_id')),
            'documentName': value.get('document_name')
        })
    return {'data': data}


@app.get('/api/specifications/{specification_id}')
def get_specification(specification_id: str):
    specification = collSpecifications.find_one({'_id': ObjectId(specification_id)})
    return {
        'id': str(specification.get('_id')),
        'documentName': specification.get('document_name'),
        'structure': [specification.get('structure')]
    }


@app.put('/api/specifications/{specification_id}')
def update_specification(specification_id: str, doc_structure: StructureDocument):
    current = {'_id': ObjectId(specification_id)}
    new_data = {'$set': {'structure': doc_structure.structure[0]}}
    collSpecifications.update_one(current, new_data)
    return 'Ok'


@app.get('/api/templates/{temp_id}')
def get_template(temp_id: str):
    template = collTemp.find_one({'_id': ObjectId(temp_id)})
    return {
        'id': str(template.get('_id')),
        'documentName': template.get('document_name'),
        'structure': [template.get('structure')]
    }


@app.post('/api/specifications')
def create_document(data: StructureCreateDocument):
    collSpecifications.insert_one({"document_name": data.name, "structure": data.structure})
    return 'Ok'
