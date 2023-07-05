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


class ColumnNotNumericError(HTTPException):
    """Raise when column not found in column_types.numeric"""
    def __init__(self, column_name: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Column {column_name} not found in column_types.numeric"
        )


class ColumnNotCategoricalError(HTTPException):
    """Raise when column not found in column_types.categorical"""
    def __init__(self, column_name: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Column {column_name} not found in column_types.categorical"
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


class ApplyingMethodNotExistsError(HTTPException):
    """Raise when ApplyMethod not exists"""
    def __init__(self, method_name: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f'Method "{method_name}" not exists'
        )


class WrongApplyingMethodParamsError(HTTPException):
    """Raise when ApplyMethodParams has wrong params"""
    def __init__(self, method_name: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f'Method "{method_name}" has wrong params'
        )


class WrongApplyingMethodParamsErrorFull(HTTPException):
    """Raise when ApplyMethodParams has wrong params"""
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=message
        )


class TargetFeatureEncodingError(HTTPException):
    """Raise when trying to encode target feature"""
    def __init__(self, target_feature: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Trying to encode target feature {target_feature} - "
                   f"denied. Target feature can't be encoded. "
                   f"Make it non-target feature first."
        )


class TargetFeatureDeletingError(HTTPException):
    """Raise when trying to delete target feature"""
    def __init__(self, target_feature: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Trying to delete target feature {target_feature} - "
                   f"denied. Target feature can't be deleted. "
                   f"Make it non-target feature first."
        )


class NansInDataFrameError(HTTPException):
    """Raise when pd.DataFrame contains NaNs"""
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=message
        )