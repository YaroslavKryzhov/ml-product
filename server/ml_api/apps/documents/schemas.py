from typing import List

from pydantic import BaseModel


class DocumentDB(BaseModel):
    name: str


class ColumnMarks(BaseModel):
    numeric: List[str]
    categorical: List[str]
    target: str
