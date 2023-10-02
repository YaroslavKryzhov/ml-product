from typing import List, Optional

from pydantic import BaseModel


class TwoDimRepresentation(BaseModel):
    first_dim: List[float]
    second_dim: List[float]
    target: List[int]


class BinaryClassificationReport(BaseModel):
    accuracy: float
    recall: Optional[float]
    precision: Optional[float]
    f1: Optional[float]
    roc_auc: float
    fpr: Optional[List[float]]
    tpr: Optional[List[float]]


class MulticlassClassificationReport(BaseModel):
    accuracy: float
    recall: float
    precision: float
    f1: float
    roc_auc_weighted: float
    roc_auc_micro: float
    roc_auc_macro: float
    fpr_micro: List[float]
    tpr_micro: List[float]
    fpr_macro: List[float]
    tpr_macro: List[float]


class RegressionReport(BaseModel):
    mse: List[float]
    mae: List[float]
    rmse: List[float]
    mape: List[float]


class ClusteringReport(BaseModel):
    silhouette_score: float
    davies_bouldin_score: float
    two_dim_representation: TwoDimRepresentation


class OutlierDetectionReport(BaseModel):
    contamination: float  # доля аномалий
    two_dim_representation: TwoDimRepresentation


class DimensionalityReductionReport(BaseModel):
    explained_variance: List[float]


class ErrorReport(BaseModel):
    error_description: str
