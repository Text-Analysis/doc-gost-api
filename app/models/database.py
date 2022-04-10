from pymongo import MongoClient
from typing import List, Dict
from app.schemas.schema import Specification, SpecificationFull, StructureDocument, StructureCreateDocument
from bson.objectid import ObjectId
from fastapi import File, UploadFile
from app.models.analyze import Analyze


class Database:

    def __init__(self, uri: str):

        client = MongoClient(uri, tls=True, tlsAllowInvalidCertificates=True)
        config = client.documentsAnalysis
        self.coll_specifications = config['requirementsSpecifications']
        self.coll_templates = config['sectionTreeTemplates']

    def get_specifications(self) -> Dict[str, List[Specification]]:
        """
        :return: The method returns all documents
        """
        data: List[Specification] = []
        for value in self.coll_specifications.find({}, {'document_name': 1}):
            specification: Specification = Specification(
                id=str(value.get('_id')),
                documentName=value.get('document_name')
            )
            List.append(data, specification)

        return {'data': data}

    def get_specifications_full(self) -> Dict[str, List[SpecificationFull]]:
        """
        :return: The method returns all documents
        """
        data: List[SpecificationFull] = []
        for value in self.coll_specifications.find({}):
            specification: SpecificationFull = SpecificationFull(
                id=str(value.get('_id')),
                documentName=value.get('document_name'),
                structure=[value.get('structure')]
            )
            List.append(data, specification)
        return {'data': data}

    def get_specifications_mongo(self) -> List[Dict]:
        return list(self.coll_specifications.find({}))

    def get_specification(self, specification_id: str) -> SpecificationFull:
        """
        :param specification_id: Id document
        :return: The method returns a full document
        """
        specification = self.coll_specifications.find_one({'_id': ObjectId(specification_id)})
        specification_correct: SpecificationFull = SpecificationFull(
            id=str(specification.get('_id')),
            documentName=specification.get('document_name'),
            structure=[specification.get('structure')])

        return specification_correct

    def update_specification(self, specification_id: str, doc_structure: StructureDocument) -> str:
        """
        :param specification_id: Id document
        :param doc_structure: The new structure of document
        :return: If document was updated successfully, the method returns 'OK'
        """
        current_specification = {'_id': ObjectId(specification_id)}
        update_data = {'$set': {'structure': doc_structure.structure[0]}}

        self.coll_specifications.update_one(current_specification, update_data)

        return 'OK'

    def create_document(self, data: StructureCreateDocument) -> str:
        """
        :param data: The structure for creating a document (including name and structure)
        :return: If document was updated successfully, the method returns 'OK'
        """
        self.coll_specifications.insert_one({"document_name": data.name, "structure": data.structure[0]})

        return 'OK'

    def get_template(self, template_id: str) -> SpecificationFull:
        """
        :param template_id: Id template
        :return: The method returns an empty template
        """
        template = self.coll_templates.find_one({'_id': ObjectId(template_id)})
        specification_correct: SpecificationFull = SpecificationFull(
            id=str(template.get('_id')),
            documentName=template.get('name'),
            structure=[template.get('structure')])

        return specification_correct

    async def parse_doc_by_template(self, file: UploadFile = File(...)) -> List:
        """
        :param file: Document
        :return: Method save a structure of document in DataBase
        """
        template = self.coll_templates.find_one({"name": "default"})["structure"]

        document_structure = await Analyze().parse_doc_by_template(file=file, template=template)

        return [document_structure]
