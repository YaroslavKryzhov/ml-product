from typing import Union, Literal, Dict
from enum import Enum

from pydantic import BaseModel, validator


class AvailableModels(Enum):
    decision_tree = 'DecisionTreeClassifier'
    catboost = 'CatBoostClassifier'


class DecisionTreeClassifierParameters(BaseModel):
    criterion: Literal['gini', 'entropy'] = 'gini'
    splitter: Literal['best', 'random'] = 'best'
    max_depth: int = None
    min_samples_split: int = 2
    min_samples_leaf: int = 1
    max_features: Union[Literal['auto', 'sqrt', 'log2'], float] = None
    random_state: int = None
    max_leaf_nodes: int = None
    min_impurity_decrease: float = 0
    class_weight: Union[Literal['balanced'], Dict] = None
    ccp_alpha: float = 0

    @validator("max_depth")
    def validate_max_depth(cls, value):
        if value <= 0:
            raise ValueError('max_depth must be greater than zero.')
        return value

    @validator("ccp_alpha")
    def validate_ccp_alpha(cls, value):
        if value < 0:
            raise ValueError('ccp_alpha must be non-negative.')
        return value


class CatBoostClassifierParameters(BaseModel):
    iterations: int = None
    learning_rate: float = None
    loss_function: Literal["Logloss", "MultiClass"] = None
    depth: int = None
