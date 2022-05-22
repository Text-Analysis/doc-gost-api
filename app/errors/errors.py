class FoundException(Exception):
    def __init__(self, name: str):
        self.name = name


class ValidException(Exception):
    def __init__(self, name: str):
        self.name = name
