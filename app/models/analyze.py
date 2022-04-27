import os
from fastapi import File, UploadFile
from srsparser import Parser, LanguageProcessor, SectionsTree
from typing import List, Dict, Optional


class Analyze:

    def __init__(self):
        self.nlp = LanguageProcessor()

    @staticmethod
    def save_file(filename: str, data):
        with open(os.path.join('app', filename), 'wb') as f:
            f.write(data)

    async def parse_doc_by_template(self, template: Dict, file: UploadFile = File(...)) -> dict:
        """
        :param file: Document
        :param template: Template
        :return: Method parse document
        """

        contents = await file.read()
        self.save_file(file.filename, contents)

        parser = Parser(template)
        document_structure = parser.parse_docx(f'./app/{file.filename}')

        os.remove(f'./app/{file.filename}')

        return document_structure

    @staticmethod
    def get_sections(structure: Dict) -> List[str]:
        structure = SectionsTree(structure)

        return structure.get_section_names()

    @staticmethod
    def check_template(structure: Dict) -> bool:
        try:
            tree = SectionsTree(structure)
            return tree.validate()
        except AssertionError:
            return False

    def get_keywords_by_specification_id(self, specifications: List[Dict], doc_name: str,
                                         mode: str, section: Optional[str] = None) -> List:
        """
        :param specifications: list of specifications
        :param doc_name: name of document
        :param mode: mode takes next variants: tf_idf, pullenti, combine
        :param section: section of document
        :return: Method returns list of specification keywords
        """
        if mode == 'combine':
            if section is None:
                return self.nlp.get_structure_rationized_keywords(specifications, doc_name)
            return self.nlp.get_structure_rationized_keywords(specifications, doc_name, section)

        if mode == 'pullenti':
            if section is None:
                return self.nlp.get_structure_keywords_pullenti(specifications, doc_name)
            return self.nlp.get_structure_keywords_pullenti(specifications, doc_name, section)

        if mode == 'tf_idf':
            if section is None:
                return self.nlp.get_structure_tf_idf_pairs(specifications, doc_name)
            return self.nlp.get_structure_tf_idf_pairs(specifications, doc_name, section)

        return []
