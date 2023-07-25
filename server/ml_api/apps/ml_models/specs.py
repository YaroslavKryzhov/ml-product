from enum import Enum


class AvailableTaskTypes(Enum):
    CLASSIFICATION = 'classification'
    REGRESSION = 'regression'
    CLUSTERING = 'clustering'
    OUTLIER_DETECTION = 'oulier_detection'
    DIMENSIONALITY_REDUCTION = 'demensionality_reduction'


class AvailableParamsTypes(Enum):
    AUTO = 'auto'
    CUSTOM = 'custom'
    DEFAULT = 'default'


class AvailableCompositionTypes(Enum):
    NONE = 'none'
    SIMPLE_VOTING = 'simple_voting'
    WEIGHTED_VOTING = 'weighted_voting'
    STACKING = 'stacking'


class ModelStatuses(Enum):
    BUILDING = 'Building'
    TRAINING = 'Training'
    TRAINED = 'Trained'
    PROBLEM = 'Problem'


class ModelFormats(Enum):
    ONNX = 'onnx'
    PICKLE = 'pickle'


class AvailableModelTypes(Enum):
    # TODO: group models by type
    # Decision Trees and Ensembles
    DECISION_TREE_CLASSIFIER = 'DecisionTreeClassifier'
    DECISION_TREE_REGRESSOR = 'DecisionTreeRegressor'
    RANDOM_FOREST_CLASSIFIER = 'RandomForestClassifier'
    RANDOM_FOREST_REGRESSOR = 'RandomForestRegressor'
    EXTRA_TREES_CLASSIFIER = 'ExtraTreesClassifier'
    EXTRA_TREES_REGRESSOR = 'ExtraTreesRegressor'
    GRADIENT_BOOSTING_CLASSIFIER = 'GradientBoostingClassifier'
    GRADIENT_BOOSTING_REGRESSOR = 'GradientBoostingRegressor'
    ADABOOST_CLASSIFIER = 'AdaBoostClassifier'
    ADABOOST_REGRESSOR = 'AdaBoostRegressor'
    BAGGING_CLASSIFIER = 'BaggingClassifier'
    BAGGING_REGRESSOR = 'BaggingRegressor'
    XGB_CLASSIFIER = 'XGBClassifier'
    XGB_REGRESSOR = 'XGBRegressor'
    LGBM_CLASSIFIER = 'LGBMClassifier'
    LGBM_REGRESSOR = 'LGBMRegressor'
    CAT_BOOST_CLASSIFIER = 'CatBoostClassifier'
    CAT_BOOST_REGRESSOR = 'CatBoostRegressor'

    # Linear models
    SGD_CLASSIFIER = 'SGDClassifier'
    SGD_REGRESSOR = 'SGDRegressor'
    LINEAR_SVC = 'LinearSVC'
    LINEAR_SVR = 'LinearSVR'
    SVC = 'SVC'
    SVR = 'SVR'
    LOGISTIC_REGRESSION = 'LogisticRegression'
    LINEAR_REGRESSION = 'LinearRegression'
    RIDGE = 'Ridge'
    LASSO = 'Lasso'
    ELASTIC_NET = 'ElasticNet'
    PASSIVE_AGGRESSIVE_CLASSIFIER = 'PassiveAggressiveClassifier'
    PASSIVE_AGGRESSIVE_REGRESSOR = 'PassiveAggressiveRegressor'

    # KNN models
    K_NEIGHBORS_CLASSIFIER = 'KNeighborsClassifier'
    K_NEIGHBORS_REGRESSOR = 'KNeighborsRegressor'
    RADIUS_NEIGHBORS_CLASSIFIER = 'RadiusNeighborsClassifier'
    RADIUS_NEIGHBORS_REGRESSOR = 'RadiusNeighborsRegressor'
    NEAREST_CENTROID = 'NearestCentroid'

    # Naive Bayes
    GAUSSIAN_NB = 'GaussianNB'

    # Neural Networks
    MLP_CLASSIFIER = 'MLPClassifier'
    MLP_REGRESSOR = 'MLPRegressor'

    # Ensembling methods
    VOTING_CLASSIFIER = 'VotingClassifier'
    VOTING_REGRESSOR = 'VotingRegressor'
    STACKING_CLASSIFIER = 'StackingClassifier'
    STACKING_REGRESSOR = 'StackingRegressor'

    # Clustering models
    K_MEANS = 'KMeans'
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
    T_SNE = 'TSNE'
    ISOMAP = 'Isomap'

    # Matrix factorization
    NMF = 'NMF'
    TRUNCATED_SVD = 'TruncatedSVD'

