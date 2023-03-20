from typing import Union, Literal, Optional, Tuple

from pydantic import BaseModel, validator

N_JOBS = 4


class DecisionTreeRegressorParameters(BaseModel):  # ready
    criterion: Literal['squared_error', 'friedman_mse', 'absolute_error', 'poisson'] = 'squared_error'
    splitter: Literal['best', 'random'] = 'best'
    max_depth: int = None
    min_samples_split: int = 2
    min_samples_leaf: int = 1

    @validator("max_depth")
    def validate_max_depth(cls, value):
        if value <= 0:
            raise ValueError('max_depth must be greater than zero.')
        return value

    @validator("min_samples_split")
    def validate_min_samples_split(cls, value):
        if value < 2:
            raise ValueError('min_samples_split must be 2 or greater.')
        return value

    @validator("min_samples_leaf")
    def validate_min_samples_leaf(cls, value):
        if value < 1:
            raise ValueError('min_samples_leaf must be 1 or greater.')
        return value
