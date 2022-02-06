import os
from fastapi import File, UploadFile
from srsparser import Parser
from typing import Any


class Analyze:

    @staticmethod
    def save_file(filename: str, data):
        with open(os.path.join('app', filename), 'wb') as f:
            f.write(data)

    async def parse_doc_by_template(self, template: Any, file: UploadFile = File(...)) -> dict:
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
