from typing import Union, Literal, Dict
from enum import Enum

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

