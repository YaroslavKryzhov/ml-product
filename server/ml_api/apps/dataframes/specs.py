from enum import Enum


class TaskType(Enum):
    classification = 'classification'
    regression = 'regression'


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


class AvailableFunctions(Enum):
    # GROUP 1: Обработка данных------------------------------------------------
    remove_duplicates = 'remove_duplicates'  # Удаление дубликатов
    drop_na = 'drop_na'  # Удаление пропусков
    drop_column = 'drop_column'
    miss_insert_mean_mode = (
        'miss_insert_mean_mode'  # Замена пропусков: Среднее и мода
    )
    miss_linear_imputer = (
        'miss_linear_imputer'  # Замена пропусков: Линейная модель
    )
    miss_knn_imputer = (
        'miss_knn_imputer'  # Замена пропусков: К-ближних соседей
    )

    # GROUP 2: Трансформация признаков (required: no NaN values)---------------
    standardize_features = (
        'standardize_features'  # Стандартизация цисленных признаков
    )
    ordinal_encoding = 'ordinal_encoding'  # Порядковое кодирование
    one_hot_encoding = 'one_hot_encoding'  # One-Hot кодирование (OHE)

    # GROUP 3: Удаление выбросов (required: no NaN values)---------------------
    outliers_isolation_forest = (
        'outliers_isolation_forest'  # Удаление выбросов: IsolationForest
    )
    outliers_elliptic_envelope = (
        'outliers_elliptic_envelope'  # Удаление выбросов: EllipticEnvelope
    )
    outliers_local_factor = (
        'outliers_local_factor'  # Удаление выбросов: LocalOutlierFactor
    )
    outliers_one_class_svm = (
        'outliers_one_class_svm'  # Удаление выбросов: OneClassSVM
    )
    outliers_sgd_one_class_svm = (
        'outliers_sgd_one_class_svm'  # Удаление выбросов: SGDOneClassSVM
    )

    # Временно приостановлено
    # GROUP 4: Отбор признаков (required: only numeric columns)----------------
    # fs_select_percentile = (
    #     'fs_select_percentile'  # Отбор признаков: по перцентилю
    # )
    # fs_select_k_best = 'fs_select_k_best'  # Отбор признаков: k лучших
    # fs_select_fpr = 'fs_select_fpr'  # Отбор признаков: FPR
    # fs_select_fdr = 'fs_select_fdr'  # Отбор признаков: FDR
    # fs_select_fwe = 'fs_select_fwe'  # Отбор признаков: FWE
    # fs_select_rfe = 'fs_select_rfe'  # Отбор признаков: RFE
    # fs_select_from_model = (
    #     'fs_select_from_model'  # Отбор признаков: из линейной модели
    # )
    # fs_select_pca = 'fs_select_pca'  # Отбор признаков: Метод главных компонент
