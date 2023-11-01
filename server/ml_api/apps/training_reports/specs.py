from enum import Enum


class ReportTypes(Enum):
    TRAIN = 'Train'
    VALID = 'Valid'
    ERROR = 'Error'


class ReportTaskTypes(Enum):
    BINARY_CLASSIFICATION = 'BinaryClassification'
    MULTICLASS_CLASSIFICATION = 'MulticlassClassification'
    REGRESSION = 'Regression'
    CLUSTERING = 'Clustering'
    DIMENSIONALITY_REDUCTION = 'DimensionalityReduction'
    OUTLIER_DETECTION = 'OutlierDetection'

