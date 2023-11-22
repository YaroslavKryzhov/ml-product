from enum import Enum


class AvailableTaskTypes(Enum):
    CLASSIFICATION = 'classification'
    REGRESSION = 'regression'
    CLUSTERING = 'clustering'
    OUTLIER_DETECTION = 'outlier_detection'
    DIMENSIONALITY_REDUCTION = 'dimensionality_reduction'


class AvailableParamsTypes(Enum):
    DEFAULT = 'default'
    CUSTOM = 'custom'
    HYPEROPT = 'hyperopt'


class ModelStatuses(Enum):
    BUILDING = 'Building'
    TRAINING = 'Training'
    TRAINED = 'Trained'
    PROBLEM = 'Problem'


# class ModelFormats(Enum):
#     ONNX = 'onnx'
#     PICKLE = 'pickle'
#     JOBLIB = 'joblib'


class AvailableModelTypes(Enum):
    # Classification models
    DECISION_TREE_CLASSIFIER = 'DecisionTreeClassifier'
    RANDOM_FOREST_CLASSIFIER = 'RandomForestClassifier'
    EXTRA_TREES_CLASSIFIER = 'ExtraTreesClassifier'
    GRADIENT_BOOSTING_CLASSIFIER = 'GradientBoostingClassifier'
    ADABOOST_CLASSIFIER = 'AdaBoostClassifier'
    BAGGING_CLASSIFIER = 'BaggingClassifier'
    XGB_CLASSIFIER = 'XGBClassifier'
    LGBM_CLASSIFIER = 'LGBMClassifier'
    CATBOOST_CLASSIFIER = 'CatBoostClassifier'
    SGD_CLASSIFIER = 'SGDClassifier'
    LINEAR_SVC = 'LinearSVC'
    SVC = 'SVC'
    LOGISTIC_REGRESSION = 'LogisticRegression'
    PASSIVE_AGGRESSIVE_CLASSIFIER = 'PassiveAggressiveClassifier'
    KNEIGHBORS_CLASSIFIER = 'KNeighborsClassifier'
    RADIUS_NEIGHBORS_CLASSIFIER = 'RadiusNeighborsClassifier'
    MLP_CLASSIFIER = 'MLPClassifier'

    # Regression models
    DECISION_TREE_REGRESSOR = 'DecisionTreeRegressor'
    RANDOM_FOREST_REGRESSOR = 'RandomForestRegressor'
    EXTRA_TREES_REGRESSOR = 'ExtraTreesRegressor'
    GRADIENT_BOOSTING_REGRESSOR = 'GradientBoostingRegressor'
    ADABOOST_REGRESSOR = 'AdaBoostRegressor'
    BAGGING_REGRESSOR = 'BaggingRegressor'
    XGB_REGRESSOR = 'XGBRegressor'
    LGBM_REGRESSOR = 'LGBMRegressor'
    CATBOOST_REGRESSOR = 'CatBoostRegressor'
    SGD_REGRESSOR = 'SGDRegressor'
    LINEAR_SVR = 'LinearSVR'
    SVR = 'SVR'
    LINEAR_REGRESSION = 'LinearRegression'
    RIDGE = 'Ridge'
    LASSO = 'Lasso'
    ELASTIC_NET = 'ElasticNet'
    PASSIVE_AGGRESSIVE_REGRESSOR = 'PassiveAggressiveRegressor'
    K_NEIGHBORS_REGRESSOR = 'KNeighborsRegressor'
    RADIUS_NEIGHBORS_REGRESSOR = 'RadiusNeighborsRegressor'
    MLP_REGRESSOR = 'MLPRegressor'

    # Clustering models
    KMEANS = 'KMeans'
    MINI_BATCH_KMEANS = 'MiniBatchKMeans'
    AFFINITY_PROPAGATION = 'AffinityPropagation'
    MEAN_SHIFT = 'MeanShift'
    SPECTRAL_CLUSTERING = 'SpectralClustering'
    WARD = 'Ward'
    AGGLOMERATIVE_CLUSTERING = 'AgglomerativeClustering'
    DBSCAN = 'DBSCAN'
    OPTICS = 'OPTICS'
    BIRCH = 'Birch'
    GAUSSIAN_MIXTURE = 'GaussianMixture'

    # Anomaly detection models
    ONE_CLASS_SVM = 'OneClassSVM'
    SGD_ONE_CLASS_SVM = 'SGDOneClassSVM'
    ELLIPTIC_ENVELOPE = 'EllipticEnvelope'
    LOCAL_OUTLIER_FACTOR = 'LocalOutlierFactor'
    ISOLATION_FOREST = 'IsolationForest'

    # Dimensionality reduction models
    PCA = 'PCA'
    LINEAR_DISCRIMINANT_ANALYSIS = 'LinearDiscriminantAnalysis'
    TSNE = 'TSNE'
    ISOMAP = 'Isomap'
    NMF = 'NMF'
    TRUNCATED_SVD = 'TruncatedSVD'

    # Ensembling methods
    VOTING_CLASSIFIER = 'VotingClassifier'
    VOTING_REGRESSOR = 'VotingRegressor'
    STACKING_CLASSIFIER = 'StackingClassifier'
    STACKING_REGRESSOR = 'StackingRegressor'
