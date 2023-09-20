from pydantic import BaseModel, Field, conint
from typing import Optional, Literal, Union


class KMeansParams(BaseModel):
    n_clusters: int = 8
    init: Literal['k-means++', 'random'] = 'k-means++'
    n_init: int = 10
    max_iter: int = 300
    tol: float = 1e-4
    precompute_distances: Literal['auto', True, False] = 'auto'
    verbose: int = 0
    random_state: Optional[int] = None
    copy_x: bool = True
    algorithm: Literal['auto', 'full', 'elkan'] = 'auto'


class MiniBatchKMeansParams(BaseModel):
    n_clusters: int = 8
    init: Literal['k-means++', 'random'] = 'k-means++'
    max_iter: int = 100
    batch_size: int = 100
    verbose: int = 0
    compute_labels: bool = True
    random_state: Optional[int] = None
    tol: float = 1e-3
    max_no_improvement: int = 10
    init_size: Optional[int] = None
    n_init: int = 3
    reassignment_ratio: float = 0.01


class AffinityPropagationParams(BaseModel):
    damping: float = 0.5
    max_iter: int = 200
    convergence_iter: int = 15
    preference: Optional[float] = None
    affinity: Literal['euclidean', 'precomputed'] = 'euclidean'
    verbose: bool = False
    random_state: Optional[int] = None


class MeanShiftParams(BaseModel):
    bandwidth: Optional[float] = None
    seeds: Optional[list] = None
    bin_seeding: bool = False
    min_bin_freq: int = 1
    cluster_all: bool = True
    n_jobs: Optional[int] = None


class SpectralClusteringParams(BaseModel):
    n_clusters: int = 8
    eigen_solver: Optional[Literal['arpack', 'lobpcg', 'amg']] = None
    random_state: Optional[int] = None
    n_init: int = 10
    gamma: float = 1.0
    affinity: Literal['nearest_neighbors', 'rbf', 'precomputed', 'precomputed_nearest_neighbors'] = 'rbf'
    n_neighbors: int = 10
    eigen_tol: float = 0.0
    degree: float = 3
    coef0: float = 1
    kernel_params: Optional[dict] = None
    n_jobs: Optional[int] = None


class WardParams(BaseModel):
    n_clusters: int = 2
    connectivity: Optional[list] = None
    compute_full_tree: Union[bool, Literal['auto']] = 'auto'
    linkage: Literal['ward', 'complete', 'average', 'single'] = 'ward'
    distance_threshold: Optional[float] = None


class AgglomerativeClusteringParams(BaseModel):
    n_clusters: Optional[int] = 2
    affinity: Literal['euclidean', 'l1', 'l2', 'manhattan', 'cosine', 'precomputed'] = 'euclidean'
    memory: Optional[str] = None
    connectivity: Optional[list] = None
    compute_full_tree: Union[bool, Literal['auto']] = 'auto'
    linkage: Literal['ward', 'complete', 'average', 'single'] = 'ward'
    distance_threshold: Optional[float] = None


class DBSCANParams(BaseModel):
    eps: float = 0.5
    min_samples: int = 5
    metric: str = 'euclidean'
    metric_params: Optional[dict] = None
    algorithm: Literal['auto', 'ball_tree', 'kd_tree', 'brute'] = 'auto'
    leaf_size: int = 30
    p: Optional[float] = None
    n_jobs: Optional[int] = None


class OPTICSParams(BaseModel):
    min_samples: int = 5
    max_eps: float = float('inf')
    metric: str = 'minkowski'
    p: int = 2
    metric_params: Optional[dict] = None
    cluster_method: Literal['xi', 'dbscan'] = 'xi'
    eps: Optional[float] = None
    xi: float = 0.05
    predecessor_correction: bool = True
    min_cluster_size: Optional[Union[int, float]] = None
    algorithm: Literal['auto', 'ball_tree', 'kd_tree', 'brute'] = 'auto'
    leaf_size: int = 30
    n_jobs: Optional[int] = None


class BirchParams(BaseModel):
    threshold: float = 0.5
    branching_factor: int = 50
    n_clusters: Optional[int] = 3
    compute_labels: bool = True


class GaussianMixtureParams(BaseModel):
    n_components: int = 1
    covariance_type: Literal['full', 'tied', 'diag', 'spherical'] = 'full'
    tol: float = 1e-3
    reg_covar: float = 1e-6
    max_iter: int = 100
    n_init: int = 1
    init_params: Literal['kmeans', 'random'] = 'kmeans'
    weights_init: Optional[list] = None
    means_init: Optional[list] = None
    precisions_init: Optional[list] = None
    random_state: Optional[int] = None
    warm_start: bool = False
    verbose: int = 0
    verbose_interval: int = 10
