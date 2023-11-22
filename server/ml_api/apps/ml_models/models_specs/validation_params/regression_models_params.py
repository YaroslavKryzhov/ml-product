from typing import Optional, Union
from pydantic import BaseModel, Field, conint, confloat
from typing import Literal


class BaseTreeRegressorParams(BaseModel):
    criterion: Literal['mse', 'friedman_mse', 'mae'] = 'mse'
    splitter: Literal['best', 'random'] = 'best'
    max_depth: Optional[conint(gt=0)] = None
    min_samples_split: conint(ge=2) = 2
    min_samples_leaf: conint(ge=1) = 1
    min_weight_fraction_leaf: float = Field(0.0, ge=0.0, le=0.5)
    max_features: Optional[str] = None
    random_state: Optional[int] = None
    max_leaf_nodes: Optional[conint(gt=0)] = None
    min_impurity_decrease: float = Field(0.0, ge=0.0)
    ccp_alpha: float = Field(0.0, ge=0.0)


class DecisionTreeRegressorParams(BaseTreeRegressorParams):
    pass


class RandomForestRegressorParams(BaseTreeRegressorParams):
    n_estimators: conint(ge=1) = 100
    bootstrap: bool = True
    oob_score: bool = False
    warm_start: bool = False


class ExtraTreesRegressorParams(BaseTreeRegressorParams):
    n_estimators: conint(ge=1) = 100
    bootstrap: bool = False
    oob_score: bool = False
    warm_start: bool = False
    max_samples: Optional[float] = None


class GradientBoostingRegressorParams(BaseModel):
    loss: Literal['ls', 'lad', 'huber', 'quantile'] = 'ls'
    learning_rate: float = Field(0.1, gt=0.0)
    n_estimators: conint(ge=1) = 100
    subsample: float = Field(1.0, ge=0.0, le=1.0)
    criterion: Literal['friedman_mse', 'mse', 'mae'] = 'friedman_mse'
    min_samples_split: conint(ge=2) = 2
    min_samples_leaf: conint(ge=1) = 1
    min_weight_fraction_leaf: float = Field(0.0, ge=0.0, le=0.5)
    max_depth: Optional[conint(gt=0)] = 3
    min_impurity_decrease: float = Field(0.0, ge=0.0)
    max_features: Optional[str] = None
    max_leaf_nodes: Optional[conint(gt=0)] = None
    random_state: Optional[int] = None
    warm_start: bool = False
    validation_fraction: float = Field(0.1, ge=0.0, le=1.0)
    n_iter_no_change: Optional[conint(ge=1)] = None
    tol: float = 1e-4


class AdaBoostRegressorParams(BaseModel):
    # base_estimator: Optional[str] = None
    n_estimators: conint(ge=1) = 50
    learning_rate: confloat(gt=0) = 1.0
    loss: Literal['linear', 'square', 'exponential'] = 'linear'
    random_state: Optional[int] = None


class BaggingRegressorParams(BaseModel):
    # base_estimator: Optional[str] = None
    n_estimators: conint(ge=1) = 10
    max_samples: conint(ge=1) = 1.0
    max_features: conint(ge=1) = 1.0
    bootstrap: bool = True
    bootstrap_features: bool = False
    oob_score: bool = False
    warm_start: bool = False
    random_state: Optional[int] = None


class XGBRegressorParams(BaseModel):
    booster: Literal['gbtree', 'gblinear', 'dart'] = 'gbtree'
    gamma: confloat(ge=0) = 0
    max_depth: conint(ge=1) = 6
    min_child_weight: confloat(ge=0) = 1
    max_delta_step: confloat(ge=0) = 0
    subsample: confloat(ge=0, le=1) = 1
    colsample_bytree: confloat(ge=0, le=1) = 1
    colsample_bylevel: confloat(ge=0, le=1) = 1
    colsample_bynode: confloat(ge=0, le=1) = 1
    reg_alpha: confloat(ge=0) = 0
    reg_lambda: confloat(ge=0) = 1
    scale_pos_weight: confloat(ge=0) = 1
    base_score: confloat(ge=0, le=1) = 0.5
    random_state: Optional[int] = None


class LGBMRegressorParams(BaseModel):
    boosting_type: Literal['gbdt', 'dart', 'goss', 'rf'] = 'gbdt'
    num_leaves: conint(ge=2) = 31
    max_depth: int = -1
    learning_rate: confloat(ge=0) = 0.1
    n_estimators: conint(ge=1) = 100
    subsample_for_bin: conint(ge=200000) = 200000
    objective: Optional[str] = None
    class_weight: Optional[str] = None
    min_split_gain: confloat(ge=0) = 0.0
    min_child_weight: confloat(ge=0) = 0.001
    min_child_samples: conint(ge=1) = 20
    subsample: confloat(ge=0, le=1) = 1.0
    subsample_freq: int = 0
    colsample_bytree: confloat(ge=0, le=1) = 1.0
    reg_alpha: confloat(ge=0) = 0.0
    reg_lambda: confloat(ge=0) = 0.0
    random_state: Optional[int] = None


class CatBoostRegressorParams(BaseModel):
    iterations: conint(ge=1) = 1000
    learning_rate: Optional[confloat(ge=0)] = None
    depth: conint(ge=1) = 6
    l2_leaf_reg: confloat(ge=0) = 3.0
    model_size_reg: confloat(ge=0) = 0.5
    rsm: Optional[confloat(ge=0, le=1)] = None
    loss_function: Literal['RMSE', 'MAE', 'Quantile', 'Poisson'] = 'RMSE'
    random_seed: Optional[int] = None
    thread_count: Optional[int] = None


class SGDRegressorParams(BaseModel):
    loss: Literal['squared_loss', 'huber', 'epsilon_insensitive', 'squared_epsilon_insensitive'] = 'squared_loss'
    penalty: Literal['none', 'l2', 'l1', 'elasticnet'] = 'none'
    alpha: confloat(ge=0) = 0.0001
    l1_ratio: confloat(ge=0, le=1) = 0.15
    fit_intercept: bool = True
    max_iter: Optional[conint(ge=1)] = None
    tol: Optional[confloat(ge=0)] = None
    shuffle: bool = True
    epsilon: confloat(ge=0) = 0.1
    random_state: Optional[int] = None
    learning_rate: Literal['constant', 'optimal', 'invscaling', 'adaptive'] = 'optimal'
    eta0: confloat(ge=0) = 0.01
    power_t: confloat(ge=0) = 0.25


class LinearSVRParams(BaseModel):
    epsilon: float = 0.0
    tol: float = 1e-4
    C: float = 1.0
    loss: Literal['epsilon_insensitive', 'squared_epsilon_insensitive'] = 'epsilon_insensitive'
    fit_intercept: bool = True
    intercept_scaling: float = 1.0
    dual: bool = True
    # verbose: int = 0
    random_state: Optional[int] = None


class SVRParams(BaseModel):
    kernel: Literal['linear', 'poly', 'rbf', 'sigmoid', 'precomputed'] = 'rbf'
    degree: conint(ge=0) = 3
    gamma: Literal['scale', 'auto'] = 'scale'
    coef0: float = 0.0
    tol: float = 1e-3
    C: float = 1.0
    epsilon: float = 0.1
    shrinking: bool = True
    # verbose: bool = False
    max_iter: int = -1


class LinearRegressionParams(BaseModel):
    fit_intercept: bool = True
    normalize: bool = False
    copy_X: bool = True
    n_jobs: Optional[int] = None


class RidgeParams(BaseModel):
    alpha: float = 1.0
    fit_intercept: bool = True
    normalize: bool = False
    copy_X: bool = True
    max_iter: Optional[int] = None
    tol: float = 1e-3
    random_state: Optional[int] = None


class LassoParams(BaseModel):
    alpha: float = 1.0
    fit_intercept: bool = True
    normalize: bool = False
    precompute: bool = False
    copy_X: bool = True
    max_iter: Optional[int] = 1000
    tol: float = 1e-4
    warm_start: bool = False
    random_state: Optional[int] = None


class ElasticNetParams(BaseModel):
    alpha: float = 1.0
    l1_ratio: float = 0.5
    fit_intercept: bool = True
    normalize: bool = False
    precompute: bool = False
    max_iter: Optional[int] = 1000
    copy_X: bool = True
    tol: float = 1e-4
    warm_start: bool = False
    random_state: Optional[int] = None


class PassiveAggressiveRegressorParams(BaseModel):
    C: float = 1.0
    fit_intercept: bool = True
    max_iter: Optional[int] = 1000
    tol: Optional[float] = 1e-3
    early_stopping: bool = False
    validation_fraction: float = 0.1
    n_iter_no_change: Optional[int] = 5
    shuffle: bool = True
    # verbose: int = 0
    loss: Literal['epsilon_insensitive', 'squared_epsilon_insensitive'] = 'epsilon_insensitive'
    epsilon: float = 0.1
    random_state: Optional[int] = None


class KNeighborsRegressorParams(BaseModel):
    n_neighbors: conint(ge=1) = 5
    weights: Literal['uniform', 'distance'] = 'uniform'
    algorithm: Literal['auto', 'ball_tree', 'kd_tree', 'brute'] = 'auto'
    leaf_size: int = 30
    p: conint(ge=1) = 2
    metric: str = 'minkowski'
    metric_params: Optional[dict] = None
    # n_jobs: Optional[int] = None


class RadiusNeighborsRegressorParams(BaseModel):
    radius: float = 1.0
    weights: Literal['uniform', 'distance'] = 'uniform'
    algorithm: Literal['auto', 'ball_tree', 'kd_tree', 'brute'] = 'auto'
    leaf_size: int = 30
    p: conint(ge=1) = 2
    metric: str = 'minkowski'
    metric_params: Optional[dict] = None
    # n_jobs: Optional[int] = None


class MLPRegressorParams(BaseModel):
    hidden_layer_sizes: tuple = (100,)
    activation: Literal['identity', 'logistic', 'tanh', 'relu'] = 'relu'
    solver: Literal['lbfgs', 'sgd', 'adam'] = 'adam'
    alpha: float = 0.0001
    batch_size: Union[int, Literal['auto']] = 'auto'
    learning_rate: Literal['constant', 'invscaling', 'adaptive'] = 'constant'
    learning_rate_init: float = 0.001
    power_t: float = 0.5
    max_iter: int = 200
    shuffle: bool = True
    random_state: Optional[int] = None
    tol: float = 1e-4
    # verbose: bool = False
    warm_start: bool = False
    momentum: float = 0.9
    nesterovs_momentum: bool = True
    early_stopping: bool = False
    validation_fraction: float = 0.1
    beta_1: float = 0.9
    beta_2: float = 0.999
    epsilon: float = 1e-8
    n_iter_no_change: int = 10
