from enum import Enum


class AvailableJobTypes(Enum):
    APPLY_METHODS = "apply_methods"
    FEATURE_IMPORTANCES = "feature_importances"
    TRAIN_MODEL = "train_model"
    BUILD_COMPOSITION = "build_composition"
    PREDICT_ON_MODEL = "predict_on_model"


class AvailableObjectTypes(Enum):
    DATAFRAME = "dataframe"
    MODEL = "model"


class JobStatuses(Enum):
    WAITING = 'waiting'
    RUNNING = 'running'
    COMPLETE = 'complete'
    ERROR = "error"
