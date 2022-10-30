from typing import Union, Literal, Dict, Optional, Tuple, List
from enum import Enum

from pydantic import BaseModel, validator

N_JOBS = 4


class AvailableModels(Enum):
    decision_tree = 'DecisionTreeClassifier'
    random_forest = 'RandomForestClassifier'
    # catboost = 'CatBoostClassifier'
    adaboost = 'AdaBoostClassifier'
    gradient_boosting = 'GradientBoostingClassifier'
    bagging = "BaggingClassifier"
    extra_trees = "ExtraTreesClassifier"
    SGD = "SGDClassifier"
    linear_SVC = "LinearSVC"
    SVC = "SVC"
    logistic_regression = 'LogisticRegression'
    perceptron = 'MLPClassifier'
    k_neighbors = 'KNeighborsClassifier'
    # xgboost = 'XGBClassifier'
    # lightgbm = 'LGBMClassifier'


class DecisionTreeClassifierParameters(BaseModel):  # ready
    criterion: Literal['gini', 'entropy'] = 'gini'
    splitter: Literal['best', 'random'] = 'best'
    max_depth: int = None
    min_samples_split: float = 2
    min_samples_leaf: int = 1
    # max_features: Union[Literal['auto', 'sqrt', 'log2'], float] = None
    # random_state: int = None
    # max_leaf_nodes: int = None
    # min_impurity_decrease: float = 0
    # class_weight: Union[Literal['balanced'], Dict] = None
    # ccp_alpha: float = 0

    @validator("max_depth")
    def validate_max_depth(cls, value):
        if value <= 0:
            raise ValueError('max_depth must be greater than zero.')
        return value

    @validator("min_samples_split")
    def validate_min_samples_split(cls, value):
        if value < 2:
            raise ValueError('min_samples_split must be 2 or greater.')
        return value

    @validator("min_samples_leaf")
    def validate_min_samples_leaf(cls, value):
        if value < 1:
            raise ValueError('min_samples_leaf must be 1 or greater.')
        return value

    # @validator("ccp_alpha")
    # def validate_ccp_alpha(cls, value):
    #     if value < 0:
    #         raise ValueError('ccp_alpha must be non-negative.')
    #     return value


class RandomForestClassifierParameters(BaseModel):  # ready
    n_estimators: int = 100
    criterion: Literal['gini', 'entropy'] = 'gini'
    max_depth: int = None
    min_samples_split: int = 2
    min_samples_leaf: int = 1
    # max_features: Union[Literal['auto', 'sqrt', 'log2'], float] = None
    # max_leaf_nodes: int = None
    # min_impurity_decrease: float = 0
    bootstrap: bool = True
    # oob_score: bool = False
    # class_weight: Union[Literal['balanced'], Dict] = None
    # ccp_alpha: float = 0

    @validator("n_estimators")
    def validate_n_estimators(cls, value):
        if value < 2:
            raise ValueError('n_estimators must be 2 or greater.')
        return value

    @validator("max_depth")
    def validate_max_depth(cls, value):
        if value <= 0:
            raise ValueError('max_depth must be greater than zero.')
        return value

    @validator("min_samples_split")
    def validate_min_samples_split(cls, value):
        if value < 2:
            raise ValueError('min_samples_split must be 2 or greater.')
        return value

    @validator("min_samples_leaf")
    def validate_min_samples_leaf(cls, value):
        if value < 1:
            raise ValueError('min_samples_leaf must be 1 or greater.')
        return value

    # @validator("ccp_alpha")
    # def validate_ccp_alpha(cls, value):
    #     if value < 0:
    #         raise ValueError('ccp_alpha must be non-negative.')
    #     return value


#
# class CatBoostClassifierParameters(BaseModel):
#     iterations: int = None
#     learning_rate: float = None
#     loss_function: Literal["Logloss", "MultiClass"] = None
#     depth: int = None


class AdaBoostClassifierParameters(BaseModel):  # ready
    # base_estimator: Optional[ClassifierMixin] = None
    n_estimators: int = 50
    learning_rate: float = 1
    algorithm: Literal['SAMME', 'SAMME.R'] = 'SAMME.R'
    # random_state: Optional[int] = None

    @validator("n_estimators")
    def validate_n_estimators(cls, value):
        if value < 2:
            raise ValueError('n_estimators must be 2 or greater.')
        return value

    @validator("learning_rate")
    def validate_learning_rate(cls, value):
        if value <= 0:
            raise ValueError('learning_rate must be greater than zero.')
        return value


class GradientBoostingClassifierParameters(BaseModel):  # ready
    loss: Literal['log_loss', 'deviance', 'exponential'] = 'deviance'
    learning_rate: float = 0.1
    n_estimators: int = 100
    subsample: float = 1
    criterion: Literal[
        'friedman_mse', 'squared_error', 'mse', 'mae'
    ] = 'friedman_mse'
    min_samples_split: Union[int, float] = 2
    # min_weight_fraction_leaf: float = 0
    max_depth: int = 3
    # min_impurity_decrease: float = 0
    # random_state: Optional[int] = None
    # max_features: Optional[
    #     Union[Literal['auto', 'sqrt', 'log2'], int, float]
    # ] = None
    # verbose: int = 0
    # max_leaf_nodes: Optional[int] = None
    # warm_start: bool = False
    # validation_fraction: float = 0.1
    # n_iter_no_change: Optional[int] = None
    # tol: float = 1e-4
    # ccp_alpha: float = 0

    @validator("learning_rate")
    def validate_learning_rate(cls, value):
        if value <= 0:
            raise ValueError('learning_rate must be greater than zero.')
        return value

    @validator("n_estimators")
    def validate_n_estimators(cls, value):
        if value < 2:
            raise ValueError('n_estimators must be 2 or greater.')
        return value

    @validator("subsample")
    def validate_subsample(cls, value):
        if value > 1 or value <= 0:
            raise ValueError("subsample must be in (0, 1]")
        return value

    @validator("min_samples_split")
    def validate_min_samples_split(cls, value):
        if value < 2:
            raise ValueError('min_samples_split must be 2 or greater.')
        return value

    # @validator("min_weight_fraction_leaf")
    # def validate_min_weight_fraction_leaf(cls, value):
    #     if value <= 0:
    #         raise ValueError(
    #             'min_weight_fraction_leaf must be greater than zero.'
    #         )
    #     return value

    @validator("max_depth")
    def validate_max_depth(cls, value):
        if value <= 0:
            raise ValueError('max_depth must be greater than zero.')
        return value

    # @validator("verbose")
    # def validate_verbose(cls, value):
    #     if value < 0:
    #         raise ValueError('verbose musth be non-negative.')
    #     return value
    #
    # @validator("max_leaf_nodes")
    # def validate_max_leaf_nodes(cls, value):
    #     if not value is None and value <= 0:
    #         raise ValueError('max_leaf_nodes must be greater than zero.')
    #     return value
    #
    # @validator("validation_fraction")
    # def validate_validation_fraction(cls, value):
    #     if value > 1 or value <= 0:
    #         raise ValueError(
    #             "validation_fraction must be between zero and one"
    #         )
    #     return value
    #
    # @validator("n_iter_no_change")
    # def validate_n_iter_no_change(cls, value):
    #     if not value is None and value < 0:
    #         raise ValueError('n_inter_no_change musth be non-negative.')
    #     return value
    #
    # @validator("tol")
    # def validate_tol(cls, value):
    #     if value < 0:
    #         raise ValueError('tol musth be non-negative.')
    #     return value
    #
    # @validator("ccp_alpha")
    # def validate_ccp_alpha(cls, value):
    #     if value < 0:
    #         raise ValueError('ccp_alpha must be non-negative.')
    #     return value


class BaggingClassifierParameters(BaseModel):  # ready
    # base_estimator: Optional[ClassifierMixin] = None
    n_estimators: int = 10
    max_samples: Union[int, float] = 1
    max_features: Union[int, float] = 1
    bootstrap: bool = True
    bootstrap_features: bool = False
    # oob_score: bool = False
    # warm_start: bool = False
    n_jobs: Optional[int] = N_JOBS  # ignore
    # random_state: Optional[int] = None
    # verbose: int = 0

    @validator("n_estimators")
    def validate_n_estimators(cls, value):
        if value < 2:
            raise ValueError('n_estimators must be 2 or greater.')
        return value

    @validator("max_samples")
    def validate_max_samples(cls, value):
        if value < 1:
            raise ValueError('max_samples must be 1 or greater.')
        return value

    @validator("max_features")
    def validate_max_features(cls, value):
        if value < 1:
            raise ValueError('max_features must be 1 or greater.')
        return value

    # @validator("n_jobs")
    # def validate_n_jobs(cls, value):
    #     if not value is None and value <= 0 and value != -1:
    #         raise ValueError(
    #             'n_jobs must be greater than zero or equal to minus one.'
    #         )
    #     return value
    #
    # @validator("verbose")
    # def validate_verbose(cls, value):
    #     if value < 0:
    #         raise ValueError('verbose musth be non-negative.')


class ExtraTreesClassifierParameters(BaseModel):  # ready
    n_estimators: int = 100
    criterion: Literal['gini', 'entropy'] = 'gini'
    max_depth: Optional[int] = None
    min_samples_split: Union[int, float] = 2
    min_samples_leaf: Union[int, float] = 1
    # min_weight_fraction_leaf: float = 0
    # max_features: Optional[
    #     Union[Literal['auto', 'sqrt', 'log2'], int, float]
    # ] = 'auto'
    # max_leaf_nodes: Optional[int] = None
    # min_impurity_decrease: float = 0
    bootstrap: bool = False
    # oob_score: bool = False
    n_jobs: Optional[int] = N_JOBS  # ignore
    # random_state: Optional[int] = None
    # verbose: int = 0
    # warm_start: bool = False
    # class_weight: Optional[
    #     Union[Literal['balanced', 'balanced_subsample'], Dict, List[Dict]]
    # ] = None
    # ccp_alpha: float = 0
    # max_samples: Optional[Union[int, float]] = None

    @validator("n_estimators")
    def validate_n_estimators(cls, value):
        if value < 2:
            raise ValueError('n_estimators must be 2 or greater.')
        return value

    @validator("max_depth")
    def validate_max_depth(cls, value):
        if value <= 0:
            raise ValueError('max_depth must be greater than zero.')
        return value

    @validator("min_samples_split")
    def validate_min_samples_split(cls, value):
        if value < 2:
            raise ValueError('min_samples_split must be 2 or greater.')
        return value

    @validator("min_samples_leaf")
    def validate_min_samples_leaf(cls, value):
        if value < 1:
            raise ValueError('min_samples_leaf must be 1 or greater.')
        return value

    # @validator("min_weight_fraction_leaf")
    # def validate_min_weight_fraction_leaf(cls, value):
    #     if value <= 0:
    #         raise ValueError(
    #             'min_weight_fraction_leaf must be greater than zero.'
    #         )
    #     return value
    #
    # @validator("max_leaf_nodes")
    # def validate_max_leaf_nodes(cls, value):
    #     if not value is None and value <= 0:
    #         raise ValueError('max_leaf_nodes must be greater than zero.')
    #     return value
    #
    # @validator("n_jobs")
    # def validate_n_jobs(cls, value):
    #     if not value is None and value <= 0 and value != -1:
    #         raise ValueError(
    #             'max_features must be greater than zero or equal to minus one.'
    #         )
    #     return value
    #
    # @validator("verbose")
    # def validate_verbose(cls, value):
    #     if value < 0:
    #         raise ValueError('verbose musth be non-negative.')
    #     return value
    #
    # @validator("ccp_alpha")
    # def validate_ccp_alpha(cls, value):
    #     if value < 0:
    #         raise ValueError('ccp_alpha must be non-negative.')
    #     return value
    #
    # @validator("max_samples")
    # def validate_max_samples(cls, value):
    #     if not value is None and value <= 0:
    #         raise ValueError('max_samples must be greater than zero.')
    #     return value


class SGDClassifierParameters(BaseModel):  # ready
    loss: Literal[
        'hinge',
        'log',
        'modified_huber',
        'squared_hinge',
        'perceptron',
        'squared_error',
        'huber',
        'epsilon_insensitive',
        'squared_epsilon_insensitive',
    ] = 'hinge'
    penalty: Literal['l2', 'l1', 'elasticnet'] = 'l2'
    alpha: float = 0.0001
    l1_ratio: float = 0.15
    fit_intercept: bool = True
    max_iter: int = 1000
    # tol: float = 1e-3
    shuffle: bool = True
    # verbose: int = 0
    epsilon: float = 0.1
    n_jobs: Optional[int] = N_JOBS  # ignore
    # random_state: int = None
    learning_rate: Literal[
        'constant', 'optimal', 'invscaling', 'adaptive'
    ] = 'optimal'
    # eta0: float = 0.0
    # power_t: float = 0.5
    # early_stopping: bool = False
    # validation_fraction: float = 0.1
    # n_iter_no_change: int = 5
    # class_weight: Union[Literal['balanced'], Dict] = None
    # warm_start: bool = False
    # average: Union[bool, int] = False

    @validator("alpha")
    def validate_alpha(cls, value):
        if value < 0:
            raise ValueError('alpha must be non-negative.')
        return value

    @validator("l1_ratio")
    def validate_l1_ratio(cls, value):
        if value < 0 or value > 1:
            raise ValueError('l1_ratio must be in [0, 1].')
        return value

    @validator("max_iter")
    def validate_max_iter(cls, value):
        if value <= 0:
            raise ValueError('max_iter must be greater than zero.')
        return value

    # @validator("tol")
    # def validate_tol(cls, value):
    #     if value < 0:
    #         raise ValueError('tol must be non-negative.')
    #     return value
    #
    # @validator("verbose")
    # def validate_verbose(cls, value):
    #     if value < 0:
    #         raise ValueError('verbose must be non-negative.')
    #     return value

    @validator("epsilon")
    def validate_epsilon(cls, value):
        if value < 0:
            raise ValueError('epsilon must be non-negative.')
        return value

    # @validator("n_jobs")
    # def validate_n_jobs(cls, value):
    #     if not value is None and value <= 0 and value != -1:
    #         raise ValueError(
    #             'n_jobs must be greater than zero or equal to minus one.'
    #         )
    #     return value
    #
    # @validator("eta0")
    # def validate_eta0(cls, value):
    #     if value < 0:
    #         raise ValueError('eta0 must be non-negative.')
    #     return value
    #
    # @validator("power_t")
    # def validate_power_t(cls, value):
    #     if value < 0:
    #         raise ValueError('power_t must be non-negative.')
    #     return value
    #
    # @validator("validation_fraction")
    # def validate_validation_fraction(cls, value):
    #     if value <= 0 or value >= 1:
    #         raise ValueError(
    #             'validation_fraction must be between zero(non-including) and one(non-including).'
    #         )
    #     return value
    #
    # @validator("n_iter_no_change")
    # def validate_n_iter_no_change(cls, value):
    #     if value <= 0:
    #         raise ValueError('n_iter_no_change must be greater than zero.')
    #     return value


class LinearSVCParameters(BaseModel):  # ready
    penalty: Literal['l2', 'l1'] = 'l2'
    loss: Literal['hinge', 'squared_hinge'] = 'squared_hinge'
    dual: bool = True
    # tol: float = 1e-4
    C: float = 1.0
    multi_class: Literal['ovr', 'crammer_singer'] = 'ovr'
    fit_intercept: bool = True
    # intercept_scaling: float = 1
    # class_weight: Union[Literal['balanced'], Dict] = None
    # verbose: int = 0
    # random_state: Optional[int] = None
    max_iter: int = 1000

    # @validator("tol")
    # def validate_tol(cls, value):
    #     if value < 0:
    #         raise ValueError('tol must be non-negative.')
    #     return value

    @validator("C")
    def validate_c(cls, value):
        if value <= 0:
            raise ValueError('C must be greater than zero.')
        return value

    # @validator("intercept_scaling")
    # def validate_intercept_scaling(cls, value):
    #     if value < 0:
    #         raise ValueError('intercept_scaling must be non-negative.')
    #     return value
    #
    # @validator("verbose")
    # def validate_verbose(cls, value):
    #     if value < 0:
    #         raise ValueError('verbose must be non-negative.')
    #     return value
    #
    @validator("max_iter")
    def validate_max_iter(cls, value):
        if value <= 0:
            raise ValueError('max_iter must be greater than zero.')
        return value


class SVCParameters(BaseModel):  # ready
    C: float = 1.0
    kernel: Literal['linear', 'poly', 'rbf', 'sigmoid', 'precomputed'] = 'rbf'
    degree: int = 3
    gamma: Union[Literal['scale', 'auto'], float] = 'scale'
    coef0: float = 0.0
    shrinking: bool = True
    probability: bool = True  # ignore!!
    # tol: float = 1e-3
    # cache_size: float = 200
    # class_weight: Union[Literal['balanced'], Dict] = None
    # verbose: bool = False
    max_iter: int = -1
    # decision_function_shape: Literal['ovo', 'ovr'] = 'ovr'
    # break_ties: bool = False
    # random_state: Optional[int] = None

    @validator("C")
    def validate_c(cls, value):
        if value <= 0:
            raise ValueError('C must be greater than zero.')
        return value

    @validator("degree")
    def validate_degree(cls, value):
        if value < 0:
            raise ValueError('degree must be non-negative.')
        return value

    # @validator("tol")
    # def validate_tol(cls, value):
    #     if value < 0:
    #         raise ValueError('tol must be non-negative.')
    #     return value
    #
    # @validator("cache_size")
    # def validate_cache_size(cls, value):
    #     if value <= 0:
    #         raise ValueError('cache_size must be greater than zero.')
    #     return value
    #
    @validator("max_iter")
    def validate_max_iter(cls, value):
        if not value is None and value <= 0 and value != -1:
            raise ValueError(
                'max_iter must be greater than zero or equal to minus one.'
            )
        return value


class LogisticRegressionParameters(BaseModel):  # ready
    penalty: Literal['l1', 'l2', 'elasticnet', 'none'] = 'l2'
    dual: bool = False
    # tol: float = 1e-4
    C: float = 1.0
    fit_intercept: bool = True
    # intercept_scaling: float = 1
    # class_weight: Optional[Union[Literal['balanced'], Dict]] = None
    # random_state: Optional[int] = None
    solver: Literal['newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga'] = 'lbfgs'
    max_iter: int = 100
    # multi_class: Literal['auto', 'ovr', 'multinomial'] = 'auto'
    # verbose: int = 0
    # warm_start: bool = False
    l1_ratio: Optional[float] = None

    @validator("C")
    def validate_C(cls, value):
        if value <= 0:
            raise ValueError('C must be greater than zero.')
        return value

    # @validator("max_iter")
    # def validate_max_iter(cls, value):
    #     if value <= 0:
    #         raise ValueError('max_iter must be greater than zero.')
    #     return value
    #
    # @validator("verbose")
    # def validate_verbose(cls, value):
    #     if value <= 0:
    #         raise ValueError('verbose must be greater than zero.')
    #     return value

    @validator("l1_ratio")
    def validate_l1_ratio(cls, value):
        if value < 0 or value > 1:
            raise ValueError(
                'l1_ratio must be greater than 0 and less than 1.'
            )
        return value


class MLPClassifierParameters(BaseModel):
    hidden_layer_sizes: Tuple[int] = (100,)
    activation: Literal['identity', 'logistic', 'tanh', 'relu'] = 'relu'
    solver: Literal['lbfgs', 'sgd', 'adam'] = 'adam'
    alpha: float = 0.0001
    max_iter: int = 200
    learning_rate: Literal['constant', 'invscaling', 'adaptive'] = 'constant'

    @validator("hidden_layer_sizes")
    def validate_hidden_layer_sizes(cls, value):
        for el in value:
            if el <= 0:
                raise ValueError('hidden_layer_sizes must be positive numbers')
        return value

    @validator("alpha")
    def validate_alpha(cls, value):
        if value < 0:
            raise ValueError('alpha must be non-negative.')
        return value

    @validator("max_iter")
    def validate_max_iter(cls, value):
        if value <= 0:
            raise ValueError('max_iter must be greater than zero.')
        return value


class KNeighborsClassifierParameters(BaseModel):
    n_neighbors: int = 5
    weights: Literal['uniform', 'distance'] = 'uniform'
    algorithm: Literal['auto', 'ball_tree', 'kd_tree', 'brute'] = 'auto'
    metric: Literal[
        'cityblock',
        'cosine',
        'euclidean',
        'haversine',
        'l1',
        'l2',
        'manhattan',
        'nan_euclidean',
        'minkowski',
        'mahalanobis',
    ] = 'minkowski'
    n_jobs = N_JOBS  # ignore!!

    @validator("n_neighbors")
    def validate_n_neighbors(cls, value):
        if value < 1:
            raise ValueError('n_neighbors must be 1 or greater.')
        return value


# class XGBClassifierParameters(BaseModel):
#     booster: Literal['gbtree', 'gblinear', 'dart'] = 'gbtree'
#     verbosity: Literal[0, 1, 2, 3] = 1
#     validate_parameters: bool = True
#     disable_default_eval_metric: bool = False
#     learning_rate: float = 0.3
#     min_split_loss: float = 0
#     max_depth: int = 6
#     min_child_weight: float = 1
#     max_delta_step: float = 0
#     subsample: float = 1
#     sampling_method: Literal['uniform', 'gradient_based'] = 'uniform'
#     reg_lambda: float = 1
#     reg_alpha: float = 0
#     tree_method: Literal[
#         'auto', 'exact', 'approx', 'hist', 'gpu_hist'
#     ] = 'auto'
#     sketch_eps: float = 0.03
#     scale_pos_weight: float = 1
#     max_leaves: int = 0
#
#     @validator("verbosity")
#     def validate_verbosity(cls, value):
#         if value <= 0:
#             raise ValueError('verbosity must be greater than zero.')
#         return value
#
#     @validator("learning_rate")
#     def validate_learning_rate(cls, value):
#         if value < 0 or value > 1:
#             raise ValueError(
#                 'learning_rate must be greater than 0 and less than 1.'
#             )
#         return value
#
#     @validator("min_split_loss")
#     def validate_min_split_loss(cls, value):
#         if value <= 0:
#             raise ValueError('min_split_loss must be greater than zero.')
#         return value
#
#     @validator("max_depth")
#     def validate_max_depth(cls, value):
#         if value <= 0:
#             raise ValueError('max_depth must be greater than zero.')
#         return value
#
#     @validator("min_child_weight")
#     def validate_min_child_weight(cls, value):
#         if value <= 0:
#             raise ValueError('min_child_weight must be greater than zero.')
#         return value
#
#     @validator("max_delta_step")
#     def validate_(cls, value):
#         if value <= 0:
#             raise ValueError(' must be greater than zero.')
#         return value
#
#     @validator("subsample")
#     def validate_subsample(cls, value):
#         if value <= 0 or value > 1:
#             raise ValueError(
#                 'subsample must be greater than 0 and less than 1.'
#             )
#         return value
#
#     @validator("sketch_eps")
#     def validate_sketch_eps(cls, value):
#         if value < 0 or value > 1:
#             raise ValueError(
#                 'sketch_eps must be greater than 0 and less than 1.'
#             )
#         return value
#
#     @validator("scale_pos_weight")
#     def validate_scale_pos_weight(cls, value):
#         if value < 0 or value > 1:
#             raise ValueError(
#                 'scale_pos_weight must be greater than 0 and less than 1.'
#             )
#         return value
#
#     @validator("max_leaves")
#     def validate_max_leaves(cls, value):
#         if value <= 0:
#             raise ValueError('max_leaves must be greater than zero.')
#         return value
#
#
# class LGBMClassifierParameters(BaseModel):
#     boosting_type: Literal['gbdt', 'goss', 'dart', 'rf'] = 'gbdt'
#     num_leaves: int = 31
#     max_depth: int = -1
#     learning_rate: float = 0.1
#     n_estimators: int = 100
#     class_weight: Optional[Union[Literal['balanced'], Dict]] = None
#     min_split_gain: float = 0
#     min_child_weight: float = 1e-3
#     min_child_samples: int = 20
#     subsample: float = 1
#     colsample_bytree: float = 1
#     reg_lambda: float = 0
#     reg_alpha: float = 0
#     random_state: Optional[int] = None
#
#     @validator("num_leaves")
#     def validate_num_leaves(cls, value):
#         if value <= 0:
#             raise ValueError('num_leaves must be greater than zero.')
#         return value
#
#     @validator("learning_rate")
#     def validate_learning_rate(cls, value):
#         if value < 0 or value > 1:
#             raise ValueError(
#                 'learning_rate must be greater than 0 and less than 1.'
#             )
#         return value
#
#     @validator("n_estimators")
#     def validate_n_estimators(cls, value):
#         if value <= 0:
#             raise ValueError('n_estimators must be greater than zero.')
#         return value
#
#     @validator("max_depth")
#     def validate_max_depth(cls, value):
#         if value <= 0 and value != -1:
#             raise ValueError(
#                 'max_depth must be greater than zero or equal -1.'
#             )
#         return value
#
#     @validator("min_child_weight")
#     def validate_min_child_weight(cls, value):
#         if value <= 0:
#             raise ValueError('min_child_weight must be greater than zero.')
#         return value
#
#     @validator("max_delta_step")
#     def validate_max_delta_step(cls, value):
#         if value <= 0:
#             raise ValueError(' must be greater than zero.')
#         return value
#
#     @validator("subsample")
#     def validate_subsample(cls, value):
#         if value <= 0 or value > 1:
#             raise ValueError(
#                 'subsample must be greater than 0 and less than 1.'
#             )
#         return value
#
#     @validator("min_split_gain")
#     def validate_min_split_gain(cls, value):
#         if value <= 0:
#             raise ValueError('min_split_gain must be greater than zero.')
#         return value
#
#     @validator("min_child_samples")
#     def validate_min_child_samples(cls, value):
#         if value <= 0:
#             raise ValueError('min_child_samples must be greater than zero.')
#         return value
#
#     @validator("colsample_bytree")
#     def validate_colsample_bytree(cls, value):
#         if value < 0 or value > 1:
#             raise ValueError(
#                 'colsample_bytree must be greater than 0 and less than 1.'
#             )
#         return value
