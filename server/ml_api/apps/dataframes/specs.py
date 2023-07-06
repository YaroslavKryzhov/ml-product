from enum import Enum


class TaskType(Enum):
    classification = 'classification'
    regression = 'regression'
    clustering = 'clustering'
    oulier_detection = 'oulier_detection'
    demensionality_reduction = 'demensionality_reduction'


class ColumnType(Enum):
    numeric = 'numeric'
    categorical = 'categorical'


class ScoreFunc(Enum):
    chi2 = 'chi2'
    f_classif = 'f_classif'
    f_regression = 'f_regression'


class BaseSklearnModels(Enum):
    linear_regression = 'linear_regression'
    random_forest_regressor = 'random_forest_regressor'
    logistic_regression = 'logistic_regression'
    linear_svc = 'linear_svc'
    random_forest_classifier = 'random_forest_classifier'


class FeatureSelectionMethods(Enum):
    variance_threshold = 'variance_threshold'
    select_k_best = 'select_k_best'
    select_percentile = 'select_percentile'
    select_fpr = 'select_fpr'
    select_fdr = 'select_fdr'
    select_fwe = 'select_fwe'
    recursive_feature_elimination = 'recursive_feature_elimination'
    sequential_forward_selection = 'sequential_forward_selection'
    sequential_backward_selection = 'sequential_backward_selection'
    select_from_model = 'select_from_model'


class AvailableMethods(Enum):
    drop_duplicates = 'drop_duplicates'
    drop_na = 'drop_na'
    drop_columns = 'drop_columns'

    fill_mean = 'fill_mean'
    fill_median = 'fill_median'
    fill_most_frequent = 'fill_most_frequent'
    fill_custom_value = 'fill_custom_value'
    fill_bfill = 'fill_bfill'
    fill_ffill = 'fill_ffill'
    fill_interpolation = 'fill_interpolation'
    fill_linear_imputer = 'fill_linear_imputer'
    fill_knn_imputer = 'fill_knn_imputer'

    leave_n_values_encoding = 'leave_n_values_encoding'
    one_hot_encoding = 'one_hot_encoding'
    ordinal_encoding = 'ordinal_encoding'

    standard_scaler = 'standard_scaler'
    min_max_scaler = 'min_max_scaler'
    robust_scaler = 'robust_scaler'
