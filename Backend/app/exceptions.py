# app/exceptions.py

class MetaPromptError(Exception):
    """Base class for all domain errors."""


class RoleNotFoundError(MetaPromptError):
    pass


class SchemaNotFoundError(MetaPromptError):
    pass


class InvalidSchemaNameError(MetaPromptError):
    pass


class LibraryFileError(MetaPromptError):
    pass
