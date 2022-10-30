from typing import List, Union, Dict, Any, Optional
from enum import Enum
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class TaskType(Enum):
    classification = 'classification'
    regression = 'regression'


class ColumnTypes(BaseModel):
    numeric: List[str]
    categorical: List[str]
    target: Optional[str] = None
    task_type: Optional[TaskType] = None


class ColumnDescription(BaseModel):
    name: str
    type: str
    not_null_count: int
    data_type: str
    data: List[Dict]


class DocumentDescription(BaseModel):
    count: Dict
    mean: Dict
    std: Dict
    min: Dict
    first_percentile: Dict
    second_percentile: Dict
    third_percentile: Dict
    max: Dict


class PipelineElement(BaseModel):
    function_name: str
    param: Union[str, int, float] = None


class DocumentFullInfo(BaseModel):
    id: UUID
    name: str
    upload_date: datetime
    change_date: datetime
    pipeline: List[PipelineElement]
    column_types: Optional[ColumnTypes]

    class Config:
        orm_mode = True


class DocumentShortInfo(BaseModel):
    name: str
    upload_date: datetime
    change_date: datetime
    pipeline: List[PipelineElement]

    class Config:
        orm_mode = True


class ReadDocumentResponse(BaseModel):
    total: int
    records: Dict[str, List]


class ServiceResponse(BaseModel):
    status_code: int
    content: Any


class AvailableFunctions(Enum):
    # GROUP 1: Обработка данных
    remove_duplicates = 'remove_duplicates'  # Удаление дубликатов
    drop_na = 'drop_na'  # Удаление пропусков
    miss_insert_mean_mode = (
        'miss_insert_mean_mode'  # Замена пропусков: Среднее и мода
    )
    miss_linear_imputer = (
        'miss_linear_imputer'  # Замена пропусков: Линейная модель
    )
    miss_knn_imputer = (
        'miss_knn_imputer'  # Замена пропусков: К-ближних соседей
    )
    # GROUP 2: Трансформация признаков
    standardize_features = (
        'standardize_features'  # Стандартизация цисленных признаков
    )
    ordinal_encoding = 'ordinal_encoding'  # Порядковое кодирование
    one_hot_encoding = 'one_hot_encoding'  # One-Hot кодирование (OHE)
    # GROUP 3: Удаление выбросов
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
    # GROUP 4: Отбор признаков
    fs_select_percentile = (
        'fs_select_percentile'  # Отбор признаков: по перцентилю
    )
    fs_select_k_best = 'fs_select_k_best'  # Отбор признаков: k лучших
    fs_select_fpr = 'fs_select_fpr'  # Отбор признаков: FPR
    fs_select_fdr = 'fs_select_fdr'  # Отбор признаков: FDR
    fs_select_fwe = 'fs_select_fwe'  # Отбор признаков: FWE
    fs_select_rfe = 'fs_select_rfe'  # Отбор признаков: RFE
    fs_select_from_model = (
        'fs_select_from_model'  # Отбор признаков: из линейной модели
    )
    fs_select_pca = 'fs_select_pca'  # Отбор признаков: Метод главных компонент
