from pydantic import BaseModel


class DocumentDB(BaseModel):
    name: str
