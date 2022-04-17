from typing import Union, Literal, Dict
from enum import Enum

from pydantic import BaseModel, validator


class AvailableSplits(Enum):
    TRAIN_VALID = 'train/valid'
    CROSS_VALIDATION = 'cross validation'
