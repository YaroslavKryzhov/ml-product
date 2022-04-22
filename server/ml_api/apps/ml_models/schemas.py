from typing import Union, Literal, Dict, Any
from enum import Enum
from ml_api.apps.ml_models.configs.classification_models_config import AvailableModels

from pydantic import BaseModel, validator


class AvailableTaskTypes(Enum):
    CLASSIFICATION = 'classification'
    REGRESSION = 'regression'


class AvailableParams(Enum):
    AUTO = 'auto'
    CUSTOM = 'custom'
    DEFAULT = 'default'


class AvailableCompositions(Enum):
    NONE = 'none'
    SIMPLE_VOTING = 'simple_voting'
    WEIGHTED_VOTING = 'weighted_voting'
    STACKING = 'stacking'


class ModelWithParams(BaseModel):
    type: AvailableModels
    params: Dict[str, Any]

