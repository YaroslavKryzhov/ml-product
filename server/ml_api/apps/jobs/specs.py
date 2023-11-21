from enum import Enum


class AvailableJobTypes(Enum):
    APPLY_METHOD = "apply_method"
    COPY_PIPELINE = "copy_pipeline"
    FEATURE_IMPORTANCES = "feature_importances"
    TRAIN_MODEL = "train_model"
    BUILD_COMPOSITION = "build_composition"
    PREDICT_ON_MODEL = "predict_on_model"


class AvailableObjectTypes(Enum):
    DATAFRAME = "dataframe"
    MODEL = "model"


class JobStatuses(Enum):
    RUNNING = 'running'
    COMPLETE = 'complete'
    ERROR = "error"
