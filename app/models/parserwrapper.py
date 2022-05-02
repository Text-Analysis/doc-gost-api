import os
from fastapi import File, UploadFile
from srsparser import Parser, LanguageProcessor, SectionsTree
from typing import List, Optional, Tuple
import numpy


class ParserWrapper:
    """
    Wrapper for the :py:class:`Parser` class.
    """

    def __init__(self):
        # initialization of a class containing natural language processing methods
        self.langproc = LanguageProcessor()

    async def parse_docx_by_template(self, template: dict, file: UploadFile = File(...)) -> dict:
        """
        Reads .docx document and returns sections tree structure filled according to the section template and document
        content.

        :param template: the section template according to which sections are extracted from the uploaded file.
        :param file: the file uploaded by the user.
        :return: the structure of the sections of the uploaded file.
        """
        contents = await file.read()
        self.save_file(file.filename, contents)
        try:
            parser = Parser(template)
            document_structure = parser.parse_docx(f'./app/{file.filename}')
            os.remove(f'./app/{file.filename}')
            return document_structure
        except Exception:
            os.remove(f'./app/{file.filename}')
            raise Exception

    def extract_tf_idf_pairs(self, documents: List[dict], document_name: str,
                             section_name: Optional[str] = None) -> List[List[Tuple[str, numpy.float64]]]:
        """
        Extracts TF-IDF pairs from a document. The required document is searched by `document_name` among all documents.

        :param documents: a collection of documents with a template structure.
        :param document_name: The name of the document from which the TF-IDF pairs will be extracted.
        :param section_name: the name of a specific section of the structure.
        :return: TF-IDF pair list for the document.
        """
        if section_name:
            return self.langproc.get_structure_tf_idf_pairs(documents, document_name, section_name)
        return self.langproc.get_structure_tf_idf_pairs(documents, document_name)

    def extract_keywords(self, documents: List[dict], document_name: str,
                         section_name: Optional[str] = None) -> List[str]:
        """
        Extracts keywords from a document. The required document is searched by `document_name` among all documents.

        :param documents: a collection of documents with a template structure.
        :param document_name: the name of the document from which the keywords will be extracted.
        :param section_name: the name of a specific section of the structure.
        :return: keyword list.
        """
        if section_name:
            return self.langproc.get_structure_keywords_pullenti(documents, document_name, section_name)
        return self.langproc.get_structure_keywords_pullenti(documents, document_name)

    def extract_rationized_keywords(self, documents: List[dict], document_name: str,
                                    section_name: Optional[str] = None) -> List[List[Tuple[str, numpy.float64]]]:
        """
        Extracts TF-IDF keyword pairs from a document. The required document is searched by `document_name`
        among all documents.

        :param documents: a collection of documents with a template structure.
        :param document_name: The name of the document from which the rationized keywords will be extracted.
        :param section_name: the name of a specific section of the structure.
        :return: TF-IDF keyword pair list for the document.
        """
        if section_name:
            return self.langproc.get_structure_rationized_keywords(documents, document_name, section_name)
        return self.langproc.get_structure_rationized_keywords(documents, document_name)

    @staticmethod
    def save_file(filename: str, data):
        with open(os.path.join('app', filename), 'wb') as f:
            f.write(data)

    @staticmethod
    def get_section_names(structure: dict) -> List[str]:
        """
        Returns the names of the sections that make up the structure.

        :param structure: section structure.
        :return: section name list.
        """
        section_tree = SectionsTree(structure)
        return section_tree.get_section_names()

    @staticmethod
    def is_valid(structure: dict) -> bool:
        """
        Checks whether the section structure is correct (compiled according to the algorithm described in srsparser).

        :param structure: section structure.
        :return: True if valid, otherwise - False.
        """
        try:
            section_tree = SectionsTree(structure)
            return section_tree.validate()
        except AssertionError:
            return False
