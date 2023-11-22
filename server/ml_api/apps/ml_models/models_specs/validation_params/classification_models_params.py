from typing import Optional, Union
from pydantic import BaseModel, Field, conint, confloat
from typing import Literal


class BaseTreeClassifierParams(BaseModel):
    criterion: Literal['gini', 'entropy'] = 'gini'
    max_depth: Optional[conint(gt=0)] = None
    min_samples_split: conint(ge=2) = 2
    min_samples_leaf: conint(ge=1) = 1
    min_weight_fraction_leaf: float = Field(0.0, ge=0.0, le=0.5)
    max_features: Optional[str] = None
    random_state: Optional[int] = None
    max_leaf_nodes: Optional[conint(gt=0)] = None
    min_impurity_decrease: float = Field(0.0, ge=0.0)
    class_weight: Optional[Literal['balanced', 'balanced_subsample']] = None
    ccp_alpha: float = Field(0.0, ge=0.0)


class DecisionTreeClassifierParams(BaseTreeClassifierParams):
    splitter: Literal['best', 'random'] = 'best'
    pass


class RandomForestClassifierParams(BaseTreeClassifierParams):
    n_estimators: conint(ge=1) = 100
    bootstrap: bool = True
    oob_score: bool = False
    # n_jobs: Optional[int] = None
    # verbose: int = 0
    warm_start: bool = False


class ExtraTreesClassifierParams(BaseTreeClassifierParams):
    n_estimators: conint(ge=1) = 100
    bootstrap: bool = False
    oob_score: bool = False
    # n_jobs: Optional[int] = None
    # verbose: int = 0
    warm_start: bool = False
    max_samples: Optional[float] = None


class GradientBoostingClassifierParams(BaseModel):
    loss: Literal['log_loss', 'exponential'] = 'log_loss'
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
    # verbose: int = 0
    warm_start: bool = False
    validation_fraction: float = Field(0.1, ge=0.0, le=1.0)
    n_iter_no_change: Optional[conint(ge=1)] = None
    tol: float = 1e-4


class AdaBoostClassifierParams(BaseModel):
    # base_estimator: Optional[str] = None
    n_estimators: conint(ge=1) = 50
    learning_rate: confloat(gt=0) = 1.0
    algorithm: Literal['SAMME', 'SAMME.R'] = 'SAMME.R'
    random_state: Optional[int] = None


class BaggingClassifierParams(BaseModel):
    # base_estimator: Optional[str] = None
    n_estimators: conint(ge=1) = 10
    max_samples: conint(ge=1) = 1.0
    max_features: conint(ge=1) = 1.0
    bootstrap: bool = True
    bootstrap_features: bool = False
    oob_score: bool = False
    warm_start: bool = False
    # n_jobs: Optional[int] = None
    random_state: Optional[int] = None
    # verbose: int = 0


class XGBClassifierParams(BaseModel):
    booster: Literal['gbtree', 'gblinear', 'dart'] = 'gbtree'
    # n_jobs: int = 1
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


class LGBMClassifierParams(BaseModel):
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
    # n_jobs: int = -1
    importance_type: Literal['split', 'gain'] = 'split'


class CatBoostClassifierParams(BaseModel):
    iterations: conint(ge=1) = 1000
    learning_rate: Optional[confloat(ge=0)] = None
    depth: conint(ge=1) = 6
    l2_leaf_reg: confloat(ge=0) = 3.0
    model_size_reg: confloat(ge=0) = 0.5
    rsm: Optional[confloat(ge=0, le=1)] = None
    loss_function: Literal['Logloss', 'CrossEntropy', 'MultiClass', 'MultiClassOneVsAll'] = 'Logloss'
    random_seed: Optional[int] = None
    thread_count: Optional[int] = None


class SGDClassifierParams(BaseModel):
    loss: Literal['hinge', 'log', 'modified_huber', 'squared_hinge', 'perceptron'] = 'hinge'
    penalty: Literal['l2', 'l1', 'elasticnet'] = 'l2'
    alpha: confloat(ge=0) = 0.0001
    max_iter: conint(ge=1) = 1000
    tol: Optional[confloat(ge=0)] = 1e-3
    shuffle: bool = True
    # verbose: conint(ge=0) = 0
    # n_jobs: Optional[conint(ge=1)] = None
    random_state: Optional[int] = None
    learning_rate: Literal['optimal', 'constant', 'invscaling', 'adaptive'] = 'optimal'
    eta0: Optional[confloat(ge=0)] = 0.0


class LinearSVCParams(BaseModel):
    penalty: Literal['l1', 'l2'] = 'l2'
    loss: Literal['hinge', 'squared_hinge'] = 'squared_hinge'
    dual: bool = True
    tol: confloat(ge=0) = 1e-4
    C: confloat(ge=0) = 1.0
    multi_class: Literal['ovr', 'crammer_singer'] = 'ovr'
    fit_intercept: bool = True
    intercept_scaling: confloat(ge=1) = 1
    class_weight: Optional[dict] = None
    # verbose: int = 0
    random_state: Optional[int] = None
    max_iter: conint(ge=1) = 1000


class SVCParams(BaseModel):
    C: confloat(ge=0) = 1.0
    kernel: Literal['linear', 'poly', 'rbf', 'sigmoid', 'precomputed'] = 'rbf'
    degree: conint(ge=0) = 3
    gamma: Literal['scale', 'auto'] = 'scale'
    coef0: float = 0.0
    shrinking: bool = True
    probability: bool = False
    tol: confloat(ge=0) = 1e-3
    cache_size: confloat(ge=1) = 200
    class_weight: Optional[dict] = None
    # verbose: bool = False
    max_iter: int = -1
    decision_function_shape: Literal['ovo', 'ovr'] = 'ovr'
    break_ties: bool = False
    random_state: Optional[int] = None


class LogisticRegressionParams(BaseModel):
    penalty: Literal['l1', 'l2', 'elasticnet', 'none'] = 'l2'
    dual: bool = False
    tol: confloat(ge=0) = 1e-4
    C: confloat(ge=0) = 1.0
    fit_intercept: bool = True
    intercept_scaling: confloat(ge=1) = 1
    class_weight: Optional[dict] = None
    random_state: Optional[int] = None
    solver: Literal['newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga'] = 'lbfgs'
    max_iter: conint(ge=1) = 100
    multi_class: Literal['auto', 'ovr', 'multinomial'] = 'auto'
    # verbose: conint(ge=0) = 0
    warm_start: bool = False
    # n_jobs: Optional[conint(ge=1)] = None
    l1_ratio: Optional[confloat(ge=0, le=1)] = None


class PassiveAggressiveClassifierParams(BaseModel):
    C: confloat(ge=0) = 1.0
    fit_intercept: bool = True
    max_iter: Optional[conint(ge=1)] = 1000
    tol: Optional[confloat(ge=0)] = 1e-3
    early_stopping: bool = False
    validation_fraction: confloat(ge=0, le=1) = 0.1
    n_iter_no_change: conint(ge=1) = 5
    shuffle: bool = True
    # verbose: conint(ge=0) = 0
    loss: Literal['hinge', 'squared_hinge'] = 'hinge'
    # n_jobs: Optional[conint(ge=1)] = None
    random_state: Optional[int] = None
    warm_start: bool = False
    class_weight: Optional[dict] = None
    average: bool = False


class KNeighborsClassifierParams(BaseModel):
    n_neighbors: conint(ge=1) = 5
    weights: Literal['uniform', 'distance'] = 'uniform'
    algorithm: Literal['auto', 'ball_tree', 'kd_tree', 'brute'] = 'auto'
    leaf_size: conint(ge=1) = 30
    p: conint(ge=1) = 2
    metric: str = 'minkowski'
    metric_params: Optional[dict] = None
    # n_jobs: Optional[conint(ge=1)] = None


class RadiusNeighborsClassifierParams(BaseModel):
    radius: confloat(ge=0) = 1.0
    weights: Literal['uniform', 'distance'] = 'uniform'
    algorithm: Literal['auto', 'ball_tree', 'kd_tree', 'brute'] = 'auto'
    leaf_size: conint(ge=1) = 30
    p: conint(ge=1) = 2
    metric: str = 'minkowski'
    outlier_label: Optional[Union[str, int]] = None
    metric_params: Optional[dict] = None
    # n_jobs: Optional[conint(ge=1)] = None


class MLPClassifierParams(BaseModel):
    hidden_layer_sizes: tuple = (100,)
    activation: Literal['identity', 'logistic', 'tanh', 'relu'] = 'relu'
    solver: Literal['lbfgs', 'sgd', 'adam'] = 'adam'
    alpha: confloat(ge=0) = 0.0001
    batch_size: Union[conint(ge=1), Literal['auto']] = 'auto'
    learning_rate: Literal['constant', 'invscaling', 'adaptive'] = 'constant'
    learning_rate_init: confloat(ge=0) = 0.001
    power_t: confloat(ge=0) = 0.5
    max_iter: conint(ge=1) = 200
    shuffle: bool = True
    random_state: Optional[int] = None
    tol: confloat(ge=0) = 1e-4
    # verbose: bool = False
    warm_start: bool = False
    momentum: confloat(ge=0) = 0.9
    nesterovs_momentum: bool = True
    early_stopping: bool = False
    validation_fraction: confloat(gt=0, lt=1) = 0.1
    beta_1: confloat(gt=0, lt=1) = 0.9
    beta_2: confloat(gt=0, lt=1) = 0.999
    epsilon: confloat(ge=0) = 1e-8
    n_iter_no_change: conint(ge=1) = 10
