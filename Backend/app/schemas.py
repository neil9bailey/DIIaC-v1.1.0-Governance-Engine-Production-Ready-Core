from pydantic import BaseModel


class PromptRequest(BaseModel):
    role: str
    task: str
    schema_name: str


class PromptResponse(BaseModel):
    prompt: str
