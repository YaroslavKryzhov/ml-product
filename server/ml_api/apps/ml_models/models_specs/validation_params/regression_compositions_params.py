from typing import Literal
from pydantic import BaseModel


class VotingRegressorParams(BaseModel):
    voting: Literal['hard', 'soft', 'weighted'] = 'hard'


class StackingRegressorParams(BaseModel):
    final_estimator: Literal[
        'RidgeCV',
        "RandomForestRegressor",
        'GradientBoostingRegressor'
    ] = 'GradientBoostingRegressor'
