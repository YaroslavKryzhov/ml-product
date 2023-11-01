from typing import List

from fastapi import HTTPException, status
from beanie import PydanticObjectId


class WrongFileTypeError(HTTPException):
    """
    Exception raised when a file of an unsupported type is uploaded.
    """
    def __init__(self, file_type: str):
        super().__init__(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported file type: {file_type}."
        )


# REPOSITORY ERRORS -----------------------------------------------------------
class DataFrameNotFoundError(HTTPException):
    """
    Exception raised when a dataframe with the given ID is not found in the database.
    """
    def __init__(self, dataframe_id: PydanticObjectId):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dataframe with id '{dataframe_id}' not found."
        )


class DataFrameFileNotFoundError(HTTPException):
    """
    Exception raised when a file associated with a dataframe is not found.
    This is considered a critical error as it implies a data integrity issue.
    """
    def __init__(self, file_id: PydanticObjectId):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"CRITICAL: File of DataFrame with id '{file_id}' not found."
        )


class FilenameExistsUserError(HTTPException):
    """
    Exception raised when a user tries to create or rename a dataframe with
    a filename that already exists in their collection.
    """
    def __init__(self, filename: str):
        super().__init__(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"DataFrame with filename '{filename}' already exists."
        )


# DATAFRAME METADATA VALIDATION ERRORS ----------------------------------------
class DataFrameIsNotPredictionError(HTTPException):
    """
    Exception raised when an operation specific to predictions is
    attempted on a dataframe that is not a prediction.
    """
    def __init__(self, dataframe_id: PydanticObjectId):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Dataframe with id {dataframe_id} isn't a prediction."
        )


class DataFrameIsPredictionError(HTTPException):
    """
    Exception raised when an operation not allowed on predictions is
    attempted on a dataframe that is a prediction.
    """
    def __init__(self, dataframe_id: PydanticObjectId):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Dataframe with id '{dataframe_id}' is a prediction. "
                   f"You can't apply this method. Move it to active dataframes first."
        )


class DataFrameAlreadyRootError(HTTPException):
    """
    Exception raised when trying to make a dataframe root,
    but it's already a root dataframe.
    """
    def __init__(self, dataframe_id: PydanticObjectId):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Dataframe with id {dataframe_id} is already root."
        )


class TargetNotFoundSupervisedLearningError(HTTPException):
    """
    Exception raised when a target column is required for an operation
    but not found in the dataframe metadata.
    """
    def __init__(self, dataframe_id: PydanticObjectId):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Dataframe with id {dataframe_id} lacks a required target column."
        )


class SetTargetNotFoundInMetadataError(HTTPException):
    """
    Exception raised when trying to set a target column
    that is not present in the dataframe metadata.
    """
    def __init__(self, dataframe_id: PydanticObjectId, target_name: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Cannot set target_column: Column {target_name} not found "
                   f"in dataframe with id {dataframe_id}."
        )


class UnsetTargetFeatureError(HTTPException):
    """
    Exception raised when trying to unset a target column
    but the dataframe doesn't have a set target column.
    """
    def __init__(self, dataframe_id: PydanticObjectId):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Cannot unset target_column: "
                   f"Dataframe with id {dataframe_id} has no target column."
        )


# DATAFRAME METADATA - CRITICAL VALIDATION ERRORS -----------------------------
# These are severe errors indicating potential code bugs.

class UnknownTargetCriticalError(HTTPException):
    """
    Exception raised when a dataframe has a target column,
    but it is not found in the ColumnTypes.
    """
    def __init__(self, dataframe_id: PydanticObjectId):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"CRITICAL: Dataframe '{dataframe_id}' has a target column "
                   f"not present in ColumnTypes."
        )


class CategoricalColumnFoundCriticalError(HTTPException):
    """
    Exception raised when categorical columns are found when only numeric columns were expected.
    """
    def __init__(self, dataframe_id: PydanticObjectId, column_names: List[str]):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Dataframe '{dataframe_id}' contains unexpected categorical columns {column_names}. "
                   f"Only numeric columns were anticipated."
        )


class ColumnTypesNotDefinedCriticalError(HTTPException):
    """
    Exception raised when column types are not defined in the dataframe.
    This could potentially occur with prediction dataframes.
    """
    def __init__(self, dataframe_id: PydanticObjectId):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"CRITICAL: Column types not defined for dataframe '{dataframe_id}'."
        )


class ColumnsNotEqualCriticalError(HTTPException):
    """
    Exception raised when the actual columns in a dataframe do not match
    the expected columns from metadata.
    """
    def __init__(self, df_columns_list: List[str], columns_list: List[str]):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"CRITICAL: Actual columns in DataFrame {df_columns_list} "
                   f"do not match expected columns {columns_list}."
        )


# FEATURE SELECTOR AND METHOD APPLIER HTTP ERRORS -----------------------------
class SelectorMethodNotExistsError(HTTPException):
    """
    Exception raised when an unrecognized feature selection method is specified.
    """
    def __init__(self, method_name: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f'Unrecognized Feature Selection method: "{method_name}".'
        )


class SelectorProcessingError(HTTPException):
    """
    Exception raised when an error occurs during the execution of a selector method.
    """
    def __init__(self, method_name: str, err: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Error executing {method_name}: {err}"
        )


class ApplyingMethodNotExistsError(HTTPException):
    """
    Exception raised when an unrecognized apply method is specified.
    """
    def __init__(self, method_name: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f'Unrecognized Apply Method: "{method_name}".'
        )


class ApplyingMethodError(HTTPException):
    """
    Exception raised when an error occurs during the execution of an apply method.
    """
    def __init__(self, method_name: str, err: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Error executing {method_name}: {err}"
        )


class ColumnNotFoundInMetadataError(HTTPException):
    """
    Exception raised when a specified column is missing from dataframe metadata.
    """
    def __init__(self, column_name: str, method_name: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"{method_name} cannot be executed: "
                   f"Column '{column_name}' is missing in "
                   f"DataFrameMetadata column_types."
        )


class ColumnNotFoundInDataFrameError(HTTPException):
    """
    Exception raised when a specified column is missing from pandas dataframe.
    """
    def __init__(self, column_name: str, method_name: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"{method_name} cannot be executed: "
                   f"Column '{column_name}' is not present "
                   f"in the pd.Dataframe columns."
        )


class InvalidSelectorParamsError(HTTPException):
    """
    Exception raised when invalid parameters are provided to a selector method.
    """
    def __init__(self, validation_err: str, method_name: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Error in {method_name}: Invalid parameters provided. "
                   f"Validation error: {validation_err}."
        )


class InvalidMethodParamsError(HTTPException):
    """
    Exception raised when provided parameters for a method are invalid.
    """
    def __init__(self, validation_err: str, method_name: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Execution of {method_name} failed: "
                   f"Parameter validation error: {validation_err}."
        )


# FEATURE SELECTOR ERRORS (PYTHON EXCEPTIONS) ---------------------------------
class UnknownTaskTypeError(Exception):
    """
    Exception raised when an unknown task type is specified for feature selection.
    """
    def __init__(self, task_type: str):
        error_message = (
            f"Unrecognized TaskType for Feature Selection: {task_type}."
        )
        super().__init__(error_message)


class UnknownBaseEstimatorError(Exception):
    """
    Exception raised when an unrecognized base estimator is specified for feature selection.
    """
    def __init__(self, estimator: str):
        error_message = (
            f"Unrecognized BaseEstimator for Feature Selection: {estimator}."
        )
        super().__init__(error_message)


# METHOD APPLIER ERRORS (PYTHON EXCEPTIONS)------------------------------------
# These exceptions indicate issues with applying specific methods to dataframes.
class NansInDataFrameError(Exception):
    """
    Exception raised when NaN values are detected in the dataframe.
    """
    def __init__(self, nan_column_names: str, method_name: str):
        error_message = (
            f"Execution of {method_name} failed: "
            f"Detected NaN values in columns: {nan_column_names}."
        )
        super().__init__(error_message)


class ColumnNotFoundInMetadataCriticalError(Exception):
    """
    Exception raised when a specified column is missing from dataframe metadata
    after columns checking on previous steps.
    """
    def __init__(self, column_name: str, method_name: str):
        error_message = (
            f"CRITICAL: {method_name} cannot be executed: "
            f"Column '{column_name}' is missing in "
            f"DataFrameMetadata column_types while trying to delete it"
        )
        super().__init__(error_message)


class ColumnNotNumericError(Exception):
    """
    Exception raised when a method is applied to a column expected to be numeric, but is categorical.
    """
    def __init__(self, column_name: str, method_name: str):
        error_message = (
            f"Column '{column_name}' is categorical. "
            f"Applying {method_name} to it is forbidden. Consider changing the column type."
        )
        super().__init__(error_message)


class ColumnNotCategoricalError(Exception):
    """
    Exception raised when a method is applied to a column expected to be categorical, but is numeric.
    """
    def __init__(self, column_name: str, method_name: str):
        error_message = (
            f"Column '{column_name}' is numeric. "
            f"Applying {method_name} to it is forbidden. Consider changing the column type."
        )
        super().__init__(error_message)


class ColumnIsTargetFeatureError(Exception):
    """
    Exception raised when a method is applied to a column that is designated as the target feature.
    """
    def __init__(self, target_feature: str, method_name: str):
        error_message = (
            f"Column '{target_feature}' is a target feature. "
            f"Applying {method_name} to it is forbidden. Designate it as a non-target feature first."
        )
        super().__init__(error_message)


class ChangeColumnTypeError(Exception):
    """
    Exception raised when there's an error converting a column to a different type.
    """
    def __init__(self, new_type: str, column_name: str, err_desc: str):
        error_message = (
            f"Failed to convert column '{column_name}' to type '{new_type}': {err_desc}."
        )
        super().__init__(error_message)


class FillCustomValueWrongDTypeError(Exception):
    """
    Exception raised when there's a type mismatch between the custom value provided
    and the expected type for a column.
    """
    def __init__(self, column_name: str, column_dtype: str, value: str, value_dtype: str):
        error_message = (
            f"Failed to fill column '{column_name}' with value '{value}': "
            f"Type mismatch. Cannot convert '{value_dtype}' to expected type '{column_dtype}'."
        )
        super().__init__(error_message)
