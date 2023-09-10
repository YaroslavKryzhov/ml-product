from typing import Optional, Union
from pydantic import BaseModel, Field, conint, confloat
from typing import Literal

# PCA (Principal Component Analysis)
class PCAParams(BaseModel):
    n_components: Optional[Union[int, float, Literal['mle']]] = None
    copy: bool = True
    whiten: bool = False
    svd_solver: Literal['auto', 'full', 'arpack', 'randomized'] = 'auto'
    tol: float = 0.0
    iterated_power: Literal['auto', 'full'] = 'auto'
    random_state: Optional[int] = None

# LDA (Linear Discriminant Analysis)
class LinearDiscriminantAnalysisParams(BaseModel):
    solver: Literal['svd', 'lsqr', 'eigen'] = 'svd'
    shrinkage: Optional[Union[Literal['auto'], str, float]] = None
    priors: Optional[list] = None
    n_components: Optional[int] = None
    store_covariance: bool = False
    tol: float = 1.0e-4

# t-SNE (t-Distributed Stochastic Neighbor Embedding)
class TSNEParams(BaseModel):
    n_components: conint(ge=1) = 2
    perplexity: confloat(ge=0) = 30.0
    early_exaggeration: confloat(ge=0) = 12.0
    learning_rate: confloat(ge=0) = 200.0
    n_iter: conint(ge=1) = 1000
    n_iter_without_progress: conint(ge=1) = 300
    min_grad_norm: float = 1e-7
    metric: str = "euclidean"
    init: Literal["random", "pca"] = "random"
    verbose: int = 0
    random_state: Optional[int] = None
    method: Literal["barnes_hut", "exact"] = "barnes_hut"
    angle: float = 0.5

# Isomap
class IsomapParams(BaseModel):
    n_neighbors: conint(ge=1) = 5
    n_components: conint(ge=1) = 2
    eigen_solver: Literal['auto', 'arpack', 'dense'] = 'auto'
    tol: float = 0
    max_iter: Optional[conint(ge=1)] = None
    path_method: Literal['auto', 'FW', 'D'] = 'auto'
    neighbors_algorithm: Literal['auto', 'brute', 'kd_tree', 'ball_tree'] = 'auto'
    n_jobs: Optional[int] = None

# NMF (Non-negative Matrix Factorization)
class NMFParams(BaseModel):
    n_components: Optional[conint(ge=1)] = None
    init: Literal['random', 'nndsvd', 'nndsvda', 'nndsvdar', 'custom'] = 'nndsvd'
    solver: Literal['cd', 'mu'] = 'cd'
    beta_loss: Union[float, Literal['frobenius', 'kullback-leibler', 'itakura-saito']] = 'frobenius'
    tol: float = 1e-4
    max_iter: conint(ge=1) = 200
    random_state: Optional[int] = None
    alpha: float = 0.0
    l1_ratio: confloat(ge=0, le=1) = 0.0
    verbose: int = 0

# TruncatedSVD
class TruncatedSVDParams(BaseModel):
    n_components: conint(ge=1) = 2
    algorithm: Literal['arpack', 'randomized'] = 'randomized'
    n_iter: conint(ge=1) = 5
    random_state: Optional[int] = None
    tol: float = 0.0

