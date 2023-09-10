from typing import Optional, Union
from pydantic import BaseModel, Field, conint, confloat, conlist
from typing import Literal


class OneClassSVMParams(BaseModel):
    kernel: Literal['linear', 'poly', 'rbf', 'sigmoid', 'precomputed'] = 'rbf'
    degree: conint(ge=1) = 3
    gamma: Union[Literal['scale', 'auto'], float] = 'scale'
    coef0: float = 0.0
    tol: float = 1e-3
    nu: confloat(gt=0, lt=1) = 0.5
    shrinking: bool = True
    cache_size: conint(ge=1) = 200
    verbose: bool = False
    max_iter: conint(ge=-1) = -1
    random_state: Optional[int] = None


class SGDOneClassSVMParams(BaseModel):
    alpha: confloat(gt=0) = 0.0001
    fit_intercept: bool = True
    shuffle: bool = True
    verbose: int = 0
    n_iter_no_change: conint(ge=1) = 5
    random_state: Optional[int] = None


class EllipticEnvelopeParams(BaseModel):
    contamination: confloat(ge=0, le=0.5) = 0.1
    support_fraction: Optional[confloat(gt=0, lt=1)] = None
    random_state: Optional[int] = None


class LocalOutlierFactorParams(BaseModel):
    n_neighbors: conint(ge=1) = 20
    algorithm: Literal['auto', 'ball_tree', 'kd_tree', 'brute'] = 'auto'
    leaf_size: conint(ge=1) = 30
    metric: str = 'minkowski'
    p: conint(ge=1) = 2
    metric_params: Optional[dict] = None
    contamination: Union['auto', confloat(ge=0, le=0.5)] = 'auto'
    novelty: bool = False
    n_jobs: Optional[int] = None


class IsolationForestParams(BaseModel):
    n_estimators: conint(ge=1) = 100
    max_samples: Union[conint(ge=1), float] = 'auto'
    contamination: Union['auto', confloat(ge=0, le=0.5)] = 'auto'
    max_features: conint(ge=1) = 1
    bootstrap: bool = False
    n_jobs: Optional[int] = None
    random_state: Optional[int] = None
    verbose: int = 0
    warm_start: bool = False

