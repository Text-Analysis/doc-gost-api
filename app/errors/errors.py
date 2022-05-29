class ResourceNotFoundException(Exception):
    """
    This exception occurs when trying to access a non-existent document or template.
    """

    def __init__(self, name: str):
        self.name = name


class UnprocessableDataException(Exception):
    """
    This exception occurs when the server receives incorrect data from the client.
    """

    def __init__(self, name: str):
        self.name = name
