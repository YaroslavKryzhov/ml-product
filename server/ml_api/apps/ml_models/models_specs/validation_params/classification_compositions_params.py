from typing import Literal
from pydantic import BaseModel


class VotingClassifierParams(BaseModel):
    voting: Literal['hard', 'soft'] = 'hard'


class StackingClassifierParams(BaseModel):
    final_estimator: Literal[
        'LogisticRegression',
        "RandomForestClassifier",
        'GradientBoostingClassifier'
    ] = 'GradientBoostingClassifier'
