from typing import Dict, Any, List, Union, Optional
from enum import Enum
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel

from ml_api.apps.ml_models.configs.classification_models import AvailableModels


class AvailableTaskTypes(Enum):
    CLASSIFICATION = 'classification'
    # REGRESSION = 'regression'


class AvailableParams(Enum):
    AUTO = 'auto'
    CUSTOM = 'custom'
    DEFAULT = 'default'


class AvailableCompositions(Enum):
    NONE = 'none'
    SIMPLE_VOTING = 'simple_voting'
    WEIGHTED_VOTING = 'weighted_voting'
    STACKING = 'stacking'


class CompositionParams(BaseModel):
    type: AvailableModels
    params: Dict[str, Any]


class BinaryClassificationMetrics(BaseModel):
    accuracy: float
    recall: float
    precision: float
    f1: float
    roc_auc: Optional[float]
    fpr: Optional[List[float]]
    tpr: Optional[List[float]]


class MulticlassClassificationMetrics(BaseModel):
    accuracy: float
    recall: float
    precision: float
    f1: float
    roc_auc_weighted: Optional[float]
    roc_auc_micro: Optional[float]
    roc_auc_macro: Optional[float]
    fpr_micro: Optional[List[float]]
    tpr_micro: Optional[List[float]]
    fpr_macro: Optional[List[float]]
    tpr_macro: Optional[List[float]]


class CompositionReport(BaseModel):
    csv_name: str
    metrics: Union[BinaryClassificationMetrics,
                   MulticlassClassificationMetrics]


class CompositionFullInfo(BaseModel):
    id: UUID
    name: str
    csv_id: UUID
    features: List[str]
    target: str
    create_date: datetime
    task_type: AvailableTaskTypes
    composition_type: AvailableCompositions
    composition_params: Union[None, List[CompositionParams]]
    stage: str
    report: Union[None, CompositionReport]

    class Config:
        orm_mode = True


class CompositionFullInfoResponse(CompositionFullInfo):
    csv_name: str


class CompositionShortInfo(BaseModel):
    name: str
    csv_id: UUID
    features: List[str]
    target: str
    create_date: datetime
    task_type: AvailableTaskTypes
    composition_type: AvailableCompositions
    stage: str

    class Config:
        orm_mode = True


class CompositionShortInfoResponse(CompositionShortInfo):
    csv_name: str
