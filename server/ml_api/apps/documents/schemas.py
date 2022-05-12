from typing import List
from enum import Enum
from pydantic import BaseModel


class DocumentDB(BaseModel):
    name: str


class ColumnMarks(BaseModel):
    numeric: List[str]
    categorical: List[str]
    target: str


class AvailableFunctions(Enum):
    remove_duplicates = 'remove_duplicates'
    drop_na = 'drop_na'
    miss_insert_mean_mode = 'miss_insert_mean_mode'
    miss_linear_imputer = 'miss_linear_imputer'
