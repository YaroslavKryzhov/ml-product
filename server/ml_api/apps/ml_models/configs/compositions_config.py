from typing import Union, Literal, Dict
from enum import Enum

from pydantic import BaseModel, validator


class AvailableCompositions(Enum):
    SIMPLE_VOTING = 'simple_voting'
    WEIGHTED_VOTING = 'weighted_voting'
    BAGGING = 'bagging'
    STACKING = 'stacking'
