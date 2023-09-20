from typing import Dict

from pydantic import ValidationError
from fastapi import HTTPException, status
from beanie import PydanticObjectId

from ml_api.apps.ml_models import schemas, specs


class FilenameExistsUserError(HTTPException):
    """Raise when filename already exists in user's models"""
    def __init__(self, filename: str):
        super().__init__(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"A model with filename {filename} already exists."
        )


class ModelNotFoundError(HTTPException):
    """Raise when model not found"""
    def __init__(self, model_id: PydanticObjectId):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Model with id {model_id} not found."
        )


class ObjectFileNotFoundError(HTTPException):
    """Raise when file not found"""
    def __init__(self, file_id: PydanticObjectId):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"File of object with id {file_id} not found."
        )


class TargetNotFoundSupervisedLearningError(HTTPException):
    """Raise when target column not found in dataframe_metadata
    for classification/regression"""
    def __init__(self, dataframe_id: PydanticObjectId):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Dataframe with id {dataframe_id} has no target column, "
                   f"which is required for supervised learning "
                   f"(classification/regression)."
        )


class UnknownTaskTypeError(HTTPException):
    """Raise when task type is not in specs.AvailableTaskTypes"""
    def __init__(self, task_type: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Unknown task type {task_type}."
        )


class UnknownParamsTypeError(HTTPException):
    """Raise when params_type is not in specs.AvailableParamsTypes"""
    def __init__(self, params_type: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Unknown params_type {params_type}."
        )


class UnknownClassificationModelError(HTTPException):
    """Raise when classification model is unknown"""
    def __init__(self, model_type: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Unknown classification model {model_type}."
        )


class UnknownRegressionModelError(HTTPException):
    """Raise when regression model is unknown"""
    def __init__(self, model_type: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Unknown regression model {model_type}."
        )


class UnknownDimensionalityReductionModelError(HTTPException):
    """Raise when dimensionality reduction model is unknown"""
    def __init__(self, model_type: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Unknown dimensionality reduction model {model_type}."
        )


class UnknownClusteringModelError(HTTPException):
    """Raise when clustering model is unknown"""
    def __init__(self, model_type: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Unknown clustering model {model_type}."
        )


class UnknownOutlierDetectionModelError(HTTPException):
    """Raise when outlier detection model is unknown"""
    def __init__(self, model_type: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Unknown outlier detection model {model_type}."
        )


class ModelParamsValidationError(HTTPException):
    """Raise when model_params is not valid"""
    def __init__(self, model_type: specs.AvailableModelTypes,
                 model_params: Dict, error: ValidationError):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Validation error for model {model_type.value} with \n"
                   f"params {model_params}; \n"
                   f"Error: \n {error.json()}."
        )


class HyperoptModelParamsValidationError(HTTPException):
    """Raise when model_params is not valid after hyperopt"""
    def __init__(self, model_params: schemas.ModelParams,
                 error: ValidationError):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"CRITICAL!!! "
                   f"Validation error for model_params after HyperOpt: \n"
                   f"{model_params.json()}; \n"
                   f"Error: \n {error.json()}."
        )


class HyperoptTaskTypeError(HTTPException):
    """Raise when trying to use hyperopt on wrong task type"""
    def __init__(self, task_type: specs.AvailableTaskTypes):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Can't use hyperopt parameters optimisation with "
                   f"task_type of{task_type.value}"
        )


class ModelNotTrainedError(HTTPException):
    """Raise when try to save not trained model"""
    def __init__(self, model_id: PydanticObjectId):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Try to save not trained model (status != TRAINED)"
                   f" with id {model_id}."
        )


class OneClassClassificationError(HTTPException):
    """Raise when try to train classification model with only one class"""
    def __init__(self, dataframe_id: PydanticObjectId):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Only one class label in dataframe with id {dataframe_id}",
        )


class TooManyClassesClassificationError(HTTPException):
    """Raise when try to train classification model with too much classes"""
    def __init__(self, limit: int, dataframe_id: PydanticObjectId):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"More than {limit} class labels in dataframe "
                   f"with id {dataframe_id}",
        )


class ReportNotFoundError(HTTPException):
    """Raise when report not found"""
    def __init__(self, report_id: PydanticObjectId):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Report with id {report_id} not found."
        )
