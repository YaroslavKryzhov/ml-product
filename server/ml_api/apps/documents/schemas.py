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

    standardize_features = 'standardize_features'
    ordinal_encoding = 'ordinal_encoding'
    one_hot_encoding = 'one_hot_encoding'

    outliers_isolation_forest = 'outliers_isolation_forest'
    outliers_elliptic_envelope = 'outliers_elliptic_envelope'
    outliers_local_factor = 'outliers_local_factor'
    outliers_one_class_svm = 'outliers_one_class_svm'
