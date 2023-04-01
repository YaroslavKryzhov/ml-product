from typing import Dict, Any, List, Union, Optional
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel

from ml_api.apps.ml_models.specs import AvailableCompositionTypes, \
    AvailableTaskTypes, CompositionStatuses, AvailableModelTypes, \
    ModelSaveFormats


class CompositionParams(BaseModel):
    type: AvailableModelTypes
    params: Dict[str, Any]


class ClassificationMetrics(BaseModel):
    accuracy: float
    recall: float
    precision: float
    f1: float
    roc_auc: Optional[float]
    fpr: Optional[List[float]]
    tpr: Optional[List[float]]
    roc_auc_weighted: Optional[float]
    roc_auc_micro: Optional[float]
    roc_auc_macro: Optional[float]
    fpr_micro: Optional[List[float]]
    tpr_micro: Optional[List[float]]
    fpr_macro: Optional[List[float]]
    tpr_macro: Optional[List[float]]


class RegeressionMetrics(BaseModel):
    # TODO: add regression
    mse: float
    mae: float
    rmse: float
    mape: float


class CompositionInfo(BaseModel):
    id: UUID
    filename: str
    user_id: UUID
    dataframe_id: UUID
    features: List[str]
    target: str
    created_at: datetime
    task_type: AvailableTaskTypes
    composition_type: AvailableCompositionTypes
    composition_params: List[CompositionParams]
    status: CompositionStatuses
    report: Optional[Union[ClassificationMetrics, RegeressionMetrics]]
    save_format: ModelSaveFormats

    class Config:
        orm_mode = True
