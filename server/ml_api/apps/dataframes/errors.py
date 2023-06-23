from fastapi import HTTPException, status
from beanie import PydanticObjectId


class DataFrameNotFoundError(HTTPException):
    """Raise when dataframe not found"""
    def __init__(self, dataframe_id: PydanticObjectId):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dataframe with id {dataframe_id} not found."
        )


class FilenameExistsUserError(HTTPException):
    """Raise when filename already exists in user's dataframes"""
    def __init__(self, filename: str):
        super().__init__(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"A file with filename {filename} already exists."
        )


class NoParentIDError(HTTPException):
    """Raise when dataframe meta has no parent_id"""
    def __init__(self):
        super().__init__(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Dataframe meta has no parent_id."
        )


class ColumnNotFoundMetadataError(HTTPException):
    """Raise when column not found in dataframe_metadata"""
    def __init__(self, column_name: str, column_type: str = 'feature'):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Column {column_name} not found in {column_type} columns."
        )


class ColumnNotFoundDataFrameError(HTTPException):
    """Raise when column not found in df.columns"""
    def __init__(self, column_name: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Column {column_name} not found in df.columns"
        )


class ColumnsNotEqualError(HTTPException):
    """Raise when feature columns in dataframe_meta not equal to real in
    Dataframe"""
    def __init__(self, dataframe_id: PydanticObjectId):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Feature columns in dataframe_meta with id {dataframe_id} not equal to real in Dataframe"
            )


class TargetNotFoundError(HTTPException):
    """Raise when target column not found in dataframe_metadata"""
    def __init__(self, dataframe_id: PydanticObjectId):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Dataframe with id {dataframe_id} has no target column"
        )


class ColumnCantBeParsedError(HTTPException):
    """Raise when column can't be parsed like numeric or categorical"""
    def __init__(self, column_name: str, column_type: str, reason: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Column {column_name} can't be parsed like {column_type}.({reason})"
        )


class SelectorMethodNotExistsError(HTTPException):
    """Raise when SelectorMethod not exists"""
    def __init__(self, method_name: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f'Method "{method_name}" not exists'
        )


class WrongSelectorParamsError(HTTPException):
    """Raise when SelectorMethodParams has wrong params"""
    def __init__(self, method_name: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f'Method "{method_name}" has wrong params'
        )
