from enum import Enum


class ColumnType(Enum):
    NUMERIC = 'numeric'
    CATEGORICAL = 'categorical'


class ScoreFunc(Enum):
    CHI2 = 'chi2'
    F_CLASSIF = 'f_classif'
    F_REGRESSION = 'f_regression'


class BaseSklearnModels(Enum):
    LINEAR_REGRESSION = 'linear_regression'
    RANDOM_FOREST_REGRESSOR = 'random_forest_regressor'
    LOGISTIC_REGRESSION = 'logistic_regression'
    LINEAR_SVC = 'linear_svc'
    RANDOM_FOREST_CLASSIFIER = 'random_forest_classifier'


class FeatureSelectionMethods(Enum):
    VARIANCE_THRESHOLD = 'variance_threshold'
    SELECT_K_BEST = 'select_k_best'
    SELECT_PERCENTILE = 'select_percentile'
    SELECT_FPR = 'select_fpr'
    SELECT_FDR = 'select_fdr'
    SELECT_FWE = 'select_fwe'
    RECURSIVE_FEATURE_ELIMINATION = 'recursive_feature_elimination'
    SEQUENTIAL_FORWARD_SELECTION = 'sequential_forward_selection'
    SEQUENTIAL_BACKWARD_SELECTION = 'sequential_backward_selection'
    SELECT_FROM_MODEL = 'select_from_model'


class AvailableMethods(Enum):
    DROP_DUPLICATES = 'drop_duplicates'
    DROP_NA = 'drop_na'
    DROP_COLUMNS = 'drop_columns'

    FILL_MEAN = 'fill_mean'
    FILL_MEDIAN = 'fill_median'
    FILL_MOST_FREQUENT = 'fill_most_frequent'
    FILL_CUSTOM_VALUE = 'fill_custom_value'
    FILL_BFILL = 'fill_bfill'
    FILL_FFILL = 'fill_ffill'
    FILL_INTERPOLATION = 'fill_interpolation'
    FILL_LINEAR_IMPUTER = 'fill_linear_imputer'
    FILL_KNN_IMPUTER = 'fill_knn_imputer'

    LEAVE_N_VALUES_ENCODING = 'leave_n_values_encoding'
    ONE_HOT_ENCODING = 'one_hot_encoding'
    ORDINAL_ENCODING = 'ordinal_encoding'

    STANDARD_SCALER = 'standard_scaler'
    MIN_MAX_SCALER = 'min_max_scaler'
    ROBUST_SCALER = 'robust_scaler'
