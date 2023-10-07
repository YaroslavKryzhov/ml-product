from enum import Enum


class ColumnType(Enum):
    NUMERIC = 'numeric'
    CATEGORICAL = 'categorical'


class FeatureSelectionTaskType(Enum):
    CLASSIFICATION = 'classification'
    REGRESSION = 'regression'


class BaseSklearnModels(Enum):
    LINEAR_REGRESSION = 'linear_regression'
    RANDOM_FOREST_REGRESSOR = 'random_forest_regressor'
    LOGISTIC_REGRESSION = 'logistic_regression'
    RANDOM_FOREST_CLASSIFIER = 'random_forest_classifier'


class FeatureSelectionMethods(Enum):
    VARIANCE_THRESHOLD = 'VarianceThreshold'
    SELECT_K_BEST = 'SelectKBest'
    SELECT_PERCENTILE = 'SelectPercentile'
    SELECT_FPR = 'SelectFpr'
    SELECT_FDR = 'SelectFdr'
    SELECT_FWE = 'SelectFwe'
    RECURSIVE_FEATURE_ELIMINATION = 'RecursiveFeatureElimination'
    SEQUENTIAL_FORWARD_SELECTION = 'SequentialForwardSelection'
    SEQUENTIAL_BACKWARD_SELECTION = 'SequentialBackwardSelection'
    SELECT_FROM_MODEL = 'SelectFromModel'


class AvailableMethods(Enum):
    DROP_DUPLICATES = 'drop_duplicates'
    DROP_NA = 'drop_na'
    DROP_COLUMNS = 'drop_columns'
    CHANGE_COLUMNS_TYPE = 'change_columns_type'

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
