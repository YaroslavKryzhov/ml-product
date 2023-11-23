from typing import Dict, List

from fastapi import HTTPException, status
from bunnet import PydanticObjectId

from ml_api.apps.ml_models import specs


class HyperoptNotAvailableError(HTTPException):
    """
    Exception raised when hyperopt is turned off.
    """
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Hyperopt params searching is turned off."
        )


# REPOSITORY ERRORS------------------------------------------------------------
# These exceptions indicate issues with accessing or managing models in a repository.
class ModelNotFoundError(HTTPException):
    """
    Exception raised when the specified model is not found in the repository.
    """
    def __init__(self, model_id: PydanticObjectId):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No model found with the id: {model_id}."
        )


class ModelFileNotFoundError(HTTPException):
    """
    Exception raised when the file corresponding to a model is not found.
    """
    def __init__(self, file_id: PydanticObjectId):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"CRITICAL: Model file with the id '{file_id}' is missing."
        )


class FilenameExistsUserError(HTTPException):
    """
    Exception raised when a filename already exists in the user's repository.
    """
    def __init__(self, filename: str):
        super().__init__(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"A model with the filename '{filename}' already exists in the repository."
        )


# MODEL METADATA VALIDATION ERRORS---------------------------------------------
# These exceptions indicate issues with validating the metadata of models.

class TargetNotFoundSupervisedLearningError(HTTPException):
    """
    Exception raised when the target column is not found in the metadata
    for classification/regression tasks.
    """
    def __init__(self, dataframe_id: PydanticObjectId):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=(
                f"Dataframe with id '{dataframe_id}' lacks a target column. "
                f"A target column is essential for supervised learning tasks."
            )
        )


class UnknownTaskTypeError(HTTPException):
    """
    Exception raised when the task type provided is not recognized.
    """
    def __init__(self, task_type: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Task type '{task_type}' is not recognized."
        )


class FeaturesNotEqualError(HTTPException):
    """
    Exception raised when there's a mismatch between features
    in the provided dataframe and the model's training dataframe.
    """
    def __init__(self, features_list_model: List[str], features_list_input: List[str]):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                f"Mismatch in features. Model was trained with: {features_list_model}. "
                f"Provided dataframe has: {features_list_input}."
            )
        )


# MODEL CONSTRUCTOR ERRORS-----------------------------------------------------
# These exceptions indicate issues during the construction of machine learning models.
class ModelConstructionError(HTTPException):
    """
    Exception raised when there's an error during model construction.
    """
    def __init__(self, err_desc: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Model construction failed: {err_desc}"
        )


# The following exceptions are raised when the provided model type is unrecognized
# for various categories of machine learning tasks.
class UnknownClassificationModelError(HTTPException):
    def __init__(self, model_type: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Unrecognized classification model type: '{model_type}'."
        )


class UnknownRegressionModelError(HTTPException):
    def __init__(self, model_type: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Unrecognized regression model type: '{model_type}'."
        )


class UnknownDimensionalityReductionModelError(HTTPException):
    def __init__(self, model_type: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Unrecognized dimensionality reduction model type: '{model_type}'."
        )


class UnknownClusteringModelError(HTTPException):
    def __init__(self, model_type: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Unrecognized clustering model type: '{model_type}'."
        )


class UnknownOutlierDetectionModelError(HTTPException):
    def __init__(self, model_type: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Unrecognized outlier detection model type: '{model_type}'."
        )

# MODEL TRAINING ERRORS--------------------------------------------------------
# These exceptions are associated with issues during model training.
class ModelTrainingError(HTTPException):
    """
    Exception raised when there's an error during the model training process.
    """
    def __init__(self, err_desc: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Model training encountered an error: {err_desc}"
        )


class OneClassClassificationError(Exception):
    """
    Exception raised when an attempt is made to train a classification model
    with only a single class label present.
    """
    def __init__(self, dataframe_id: PydanticObjectId):
        error_message = (
            f"Only one class label detected in dataframe with id {dataframe_id}. "
            f"Classification models require at least two distinct class labels."
        )
        super().__init__(error_message)


class TooManyClassesClassificationError(Exception):
    """
    Exception raised when an attempt is made to train a classification model
    with an excessive number of class labels.
    """
    def __init__(self, limit: int, dataframe_id: PydanticObjectId):
        error_message = (
            f"Dataframe with id {dataframe_id} has more than {limit} class labels, "
            f"which exceeds the allowable limit."
        )
        super().__init__(error_message)


# MODEL PREDICTION ERRORS------------------------------------------------------
# These exceptions pertain to issues encountered during model prediction.
class ModelPredictionError(HTTPException):
    """
    Exception raised when there's an error during the prediction process.
    """
    def __init__(self, err_desc: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Error encountered during model prediction: {err_desc}."
        )


# PARAMETERS SEARCHING ERRORS--------------------------------------------------
# These exceptions are related to errors during hyperparameter optimization.
class ParamsSearchingError(HTTPException):
    """
    Exception raised during the hyperparameter optimization process.
    """
    def __init__(self, model_type:str, err_desc: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Error encountered during hyperparameter optimization for model "
                   f"{model_type}: {err_desc}"
        )


class HyperoptTaskTypeError(HTTPException):
    """
    Exception raised when trying to use hyperopt on an unsuitable task type.
    """
    def __init__(self, task_type: specs.AvailableTaskTypes):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Hyperparameter optimization (hyperopt) is not supported for "
                   f"task type: {task_type.value}."
        )


# PARAMETERS VALIDATION ERRORS-------------------------------------------------
# These exceptions are associated with validation of model parameters.
class UnknownParamsTypeError(HTTPException):
    """
    Exception raised when the parameter type provided is unrecognized.
    """
    def __init__(self, params_type: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"The parameter type '{params_type}' is not recognized."
        )


class ModelParamsValidationError(HTTPException):
    """
    Exception raised when model parameters are not valid.
    """
    def __init__(self, model_type: str, model_params: Dict, validation_err: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=(
                f"Parameter validation error for model type '{model_type}':\n"
                f"Provided Parameters: {model_params}\n"
                f"Error Description: {validation_err}."
            )
        )


# COMPOSITION CONSTRUCTION ERRORS----------------------------------------------
class UnknownClassificationCompositionError(HTTPException):
    """
    Exception raised when the classification composition type provided is unrecognized.
    """
    def __init__(self, composition_type: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=(
                f"Unrecognized classification composition type: '{composition_type}'."
            )
        )


class UnknownRegressionCompositionError(HTTPException):
    """
    Exception raised when the regression composition type provided is unrecognized.
    """
    def __init__(self, composition_type: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Unrecognized regression composition type: '{composition_type}'."
        )


class CompositionConstructionError(HTTPException):
    """
    Exception raised when there's an error during composition construction.
    """
    def __init__(self, err_desc: str):
        super.__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Composition construction failed: {err_desc}"
        )


class CompositionValidationError(HTTPException):
    """
    Exception raised when there's an error during composition validation.
    """
    def __init__(self, err_desc: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Composition validation failed: {err_desc}"
        )


class UnknownCompositionTypeError(HTTPException):
    """
    Exception raised when the composition type provided is unrecognized.
    """
    def __init__(self, composition_type: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Unrecognized composition type: '{composition_type}'."
        )


class DifferentDataFramesCompositionError(HTTPException):
    """
    Exception raised when the dataframes of the models in a composition
    are not the same.
    """
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Models in a composition must have the same dataframe."
        )


class WrongTaskTypesCompositionError(HTTPException):
    """
    Exception raised when the task type of a model in a composition
    is not supported.
    """
    def __init__(self, value):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Task type {value} is not supported for composition."
        )


class DifferentTaskTypesCompositionError(HTTPException):
    """
    Exception raised when the task types of the models in a composition
    are not the same.
    """
    def __init__(self, value1, value2):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Models in a composition must have the same task type. "
                   f"Provided models have {value1} and {value2} task types."
        )


class DifferentFeatureColumnsCompositionError(HTTPException):
    """
    Exception raised when the feature columns of the models in a composition
    are not the same.
    """
    def __init__(self, feature_columns1, feature_columns2):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Models in a composition must have the same feature columns."
                   f"Provided models have {feature_columns1} and {feature_columns2}."
        )


class DifferentTargetColumnsCompositionError(HTTPException):
    """
    Exception raised when the target columns of the models in a composition
    are not the same.
    """
    def __init__(self, target_column1, target_column2):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Models in a composition must have the same target column. "
                   f"Provided models have {target_column1} and {target_column2}."
        )