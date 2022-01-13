from pymongo import MongoClient
from typing import List, Dict
from app.models import Specification, SpecificationFull, StructureDocument, StructureCreateDocument
from bson.objectid import ObjectId
from fastapi import File, UploadFile
import os
from srsparser import Parser


class Database:
    """
    Класс, с помощью которого происходит взаимодействие с базой данных MongoDB
    """

    def __init__(self, uri: str):

        client = MongoClient(uri, tls=True, tlsAllowInvalidCertificates=True)
        config = client.documentsAnalysis
        self.coll_specifications = config['requirementsSpecifications']
        self.coll_templates = config['sectionTreeTemplates']

    def get_specifications(self) -> Dict[str, List[Specification]]:
        """
        :return: Метод возвращает все документы
        """
        data: List[Specification] = []
        for value in self.coll_specifications.find({}, {'document_name': 1}):
            specification: Specification = Specification(
                id=str(value.get('_id')),
                documentName=value.get('document_name')
            )
            List.append(data, specification)

        return {'data': data}

    def get_specification(self, specification_id: str) -> SpecificationFull:
        """
        :param specification_id: Id документа
        :return: Метод возвращает целиком документ
        """
        specification = self.coll_specifications.find_one({'_id': ObjectId(specification_id)})
        specification_correct: SpecificationFull = SpecificationFull(
            id=str(specification.get('_id')),
            documentName=specification.get('document_name'),
            structure=[specification.get('structure')])

        return specification_correct

    def update_specification(self, specification_id: str, doc_structure: StructureDocument) -> str:
        """
        :param specification_id: Id документа
        :param doc_structure: Новая структура документа
        :return: Если документ успешно обновлён, метод возвращает 'OK'
        """
        current_specification = {'_id': ObjectId(specification_id)}
        update_data = {'$set': {'structure': doc_structure.structure[0]}}

        self.coll_specifications.update_one(current_specification, update_data)

        return 'OK'

    def create_document(self, data: StructureCreateDocument) -> str:
        """
        :param data: Структура для создания документа (включает название и содержание)
        :return: Если документ успешно добавлен, метод возвращает 'OK'
        """
        self.coll_specifications.insert_one({"document_name": data.name, "structure": data.structure})

        return 'OK'

    def get_template(self, template_id: str) -> SpecificationFull:
        """
        :param template_id: Id шаблона
        :return: Метод возращает пустой шаблон для создания документа
        """
        template = self.coll_templates.find_one({'_id': ObjectId(template_id)})
        specification_correct: SpecificationFull = SpecificationFull(
            id=str(template.get('_id')),
            documentName=template.get('name'),
            structure=[template.get('structure')])

        return specification_correct

    @staticmethod
    def save_file(filename: str, data):
        with open(os.path.join('app', filename), 'wb') as f:
            f.write(data)

    async def parse_doc_by_template(self, file: UploadFile = File(...)) -> str:

        template = self.coll_templates.find_one({"name": "default"})["structure"]

        contents = await file.read()
        self.save_file(file.filename, contents)

        parser = Parser(template)
        document_structure = parser.parse_docx(f'./app/{file.filename}')

        self.coll_specifications.insert_one({"document_name": file.filename, "structure": document_structure})

        os.remove(f'./app/{file.filename}')

        return 'OK'
