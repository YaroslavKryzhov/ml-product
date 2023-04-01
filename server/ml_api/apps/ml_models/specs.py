from enum import Enum


class AvailableTaskTypes(Enum):
    CLASSIFICATION = 'classification'
    REGRESSION = 'regression'


class AvailableParamsTypes(Enum):
    AUTO = 'auto'
    CUSTOM = 'custom'
    DEFAULT = 'default'


class AvailableCompositionTypes(Enum):
    NONE = 'none'
    SIMPLE_VOTING = 'simple_voting'
    WEIGHTED_VOTING = 'weighted_voting'
    STACKING = 'stacking'


class CompositionStatuses(Enum):
    BUILD = 'Building'
    TRAINING = 'Training'
    TRAINED = 'Trained'
    PROBLEM = 'Problem'


class ModelSaveFormats(Enum):
    ONNX = 'onnx'
    PICKLE = 'pickle'


class AvailableModelTypes(Enum):
    decision_tree = 'DecisionTreeClassifier'
    random_forest = 'RandomForestClassifier'
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
    # catboost = 'CatBoostClassifier'
