class PromptGeneratorError(Exception):
    """Base application error."""


class RoleNotFoundError(PromptGeneratorError):
    pass


class InvalidSchemaNameError(PromptGeneratorError):
    pass
