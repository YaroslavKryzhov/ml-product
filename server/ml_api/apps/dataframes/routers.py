from typing import List, Dict

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, UploadFile, File

from ml_api.apps.users.routers import current_active_user
from ml_api.apps.users.models import User
from ml_api.apps.dataframes.services.dataframe_service import DataframeService
from ml_api.apps.dataframes.services.methods_service import DataframeMethodsService
from ml_api.apps.dataframes import schemas, models, specs
# from ml_api.common.celery_tasks.celery_tasks import apply_function_celery, \
#     copy_pipeline_celery

dataframes_file_router = APIRouter(
    prefix="/dataframe",
    tags=["Dataframe As File"],
    responses={404: {"description": "Not found"}},
)


@dataframes_file_router.post("", summary="Загрузить csv-файл",
                             response_model=models.DataFrameMetadata)
async def upload_dataframe(
    filename: str,
    file: UploadFile = File(...),
    user: User = Depends(current_active_user),
):
    """
        Загружает файл в систему

        - **filename**: сохраняемое имя файла
        - **file**: csv-файл
    """
    return await DataframeService(user.id).upload_new_dataframe(
        file=file.file, filename=filename)


@dataframes_file_router.get("/download", summary="Скачать csv-файл")
async def download_dataframe(
    dataframe_id: PydanticObjectId,
    user: User = Depends(current_active_user),
):
    """
        Скачивает csv-файл пользователя

        - **dataframe_id**: ID csv-файла(датафрейма)
    """
    return await DataframeService(user.id).download_dataframe(dataframe_id)


@dataframes_file_router.put("/rename", summary="Переименовать csv-файл",
                             response_model=models.DataFrameMetadata)
async def rename_dataframe(
    dataframe_id: PydanticObjectId,
    new_filename: str,
    user: User = Depends(current_active_user),
):
    """
        Переименовывает csv-файл

        - **dataframe_id**: ID csv-файла(датафрейма)
        - **new_filename**: новое имя файла
    """
    return await DataframeService(user.id).set_filename(
        dataframe_id, new_filename)


@dataframes_file_router.delete("", summary="Удалить csv-файл",
                               response_model=models.DataFrameMetadata)
async def delete_dataframe(
    dataframe_id: PydanticObjectId,
    user: User = Depends(current_active_user),
):
    """
        Удаляет csv-файл

        - **dataframe_id**: ID csv-файла(датафрейма)
    """
    return await DataframeService(user.id).delete_dataframe(dataframe_id)


@dataframes_file_router.delete("/prediction",  summary="Удалить предсказание модели",
                           response_model=models.DataFrameMetadata)
async def delete_model_prediction(
    model_id: PydanticObjectId,
    prediction_id: PydanticObjectId,
    user: User = Depends(current_active_user),
):
    """
        Удаляет предсказание модели.

        - **model_id**: ID модели
    """
    return await DataframeService(user.id).delete_prediction(
        model_id, prediction_id)


dataframes_metadata_router = APIRouter(
    prefix="/dataframe/metadata",
    tags=["Dataframe Metadata"],
    responses={404: {"description": "Not found"}},
)


@dataframes_metadata_router.get("", response_model=models.DataFrameMetadata,
    summary="Получить информацию о csv-файле (датафрейме)")
async def read_dataframe_info(
    dataframe_id: PydanticObjectId,
    user: User = Depends(current_active_user),
):
    """
        Возвращает информацию о датафрейме

        - **dataframe_id**: ID csv-файла(датафрейма)
    """
    return await DataframeService(user.id).get_dataframe_meta(dataframe_id)


@dataframes_metadata_router.get("/all", response_model=List[models.DataFrameMetadata],
    summary="Получить информацию обо всех csv-файлах (датафреймах)")
async def read_all_user_dataframes(user: User = Depends(current_active_user)):
    """
        Возвращает информацию обо всех датафреймах пользователя
    """
    return await DataframeService(user.id).get_active_dataframes_meta()


dataframes_content_router = APIRouter(
    prefix="/dataframe/content",
    tags=["Dataframe Content"],
    responses={404: {"description": "Not found"}})


@dataframes_content_router.get("",
                               response_model=schemas.ReadDataFrameResponse,
                               summary="Прочитать датафрейм")
async def read_dataframe_with_pagination(
    dataframe_id: PydanticObjectId,
    page: int = 1,
    rows_on_page: int = 50,
    user: User = Depends(current_active_user),
):
    """
        Возвращает содержимое csv-файла (датафрейма) с пагинацией

        - **dataframe_id**: ID csv-файла(датафрейма)
        - **page**: номер cтраницы (default=1)
        - **rows_on_page**: кол-во строк датафрейма на cтраницу (default=1)
    """
    return await DataframeService(
        user.id).get_dataframe_with_pagination(dataframe_id, page, rows_on_page)


@dataframes_content_router.get("/statistics",
    response_model=List[schemas.ColumnDescription],
    summary="Получить описание столбцов")
async def dataframe_columns_stat_info(
    dataframe_id: PydanticObjectId,
    user: User = Depends(current_active_user),
):
    """
        Возвращает описание для всех столбцов датафрейма:

        * Имя столбца
        * Тип (численный, категориальный)
        * Количество непустых значений
        * Количество пустых значений
        * Тип данных (int, float64, object, etc.)
        * Содержание:
            * для численных – гистограмма распределения (pandas.hist())
            * для категориальных – количество значений (pandas.value_counts())
        * Дополнительная статистика

        - **dataframe_id**: ID csv-файла(датафрейма)
    """
    return await DataframeService(
        user.id).get_dataframe_column_statistics(dataframe_id)


@dataframes_content_router.get("/column_types",
                               response_model=schemas.ColumnTypes,
                               summary="Получить списки типов столбцов")
async def get_column_types(dataframe_id: PydanticObjectId,
                           user: User = Depends(current_active_user)):
    """
        Возвращает списки типов столбцов датафрейма.

        - **dataframe_id**: ID csv-файла(датафрейма)
    """
    return await DataframeService(
        user.id).get_feature_column_types(dataframe_id)


@dataframes_content_router.get("/corr_matrix",
                               response_model=Dict[str, Dict[str, float]],
                               summary="Получить матрицу корреляций")
async def get_correlation_matrix(dataframe_id: PydanticObjectId,
                                 user: User = Depends(current_active_user)):
    """
        Возвращает матрицу корреляций для численных столбцов датафрейма.

        - **dataframe_id**: ID csv-файла(датафрейма)
    """
    return await DataframeService(
        user.id).get_correlation_matrix(dataframe_id)


dataframes_methods_router = APIRouter(
    prefix="/dataframe/edit",
    tags=["Dataframe Editions"],
    responses={404: {"description": "Not found"}},
)


@dataframes_methods_router.put("/target",
                               summary="Задать целевой признак",
                               response_model=models.DataFrameMetadata)
async def set_target_feature(dataframe_id: PydanticObjectId,
                             target_column: str,
                             user: User = Depends(current_active_user)):
    """
        Помечает столбец датафрейма как целевой (Y).

        - **dataframe_id**: ID csv-файла(датафрейма)
        - **target_column**: имя целевого столбца
    """
    return await DataframeService(
        user.id).set_target_feature(dataframe_id, target_column)


@dataframes_methods_router.delete("/target",
                               summary="Очистить выбор целевого признака",
                               response_model=models.DataFrameMetadata)
async def unset_target_feature(dataframe_id: PydanticObjectId,
                             user: User = Depends(current_active_user)):
    """
        Убирает отметку столбца датафрейма как целевого (Y).

        - **dataframe_id**: ID csv-файла(датафрейма)
    """
    return await DataframeService(
        user.id).unset_target_feature(dataframe_id=dataframe_id)


@dataframes_methods_router.put("/move_to_root",
                               summary="Переместить в корень интерфейса",
                               response_model=models.DataFrameMetadata)
async def move_to_root(dataframe_id: PydanticObjectId,
                             user: User = Depends(current_active_user)):
    """
        Переносит датафрейм из вложенного уровня в корень интерфейса.

        - **dataframe_id**: ID csv-файла(датафрейма)
    """
    return await DataframeService(user.id).move_dataframe_to_root(
        dataframe_id)


@dataframes_methods_router.put("/move_to_active",
                               summary="Переместить предсказание в активные",
                               response_model=models.DataFrameMetadata)
async def move_to_active(
        model_id: PydanticObjectId,
        dataframe_id: PydanticObjectId,
        user: User = Depends(current_active_user)):
    """
        Переносит датафрейм из раздела предсказаний в корень интерфейса.

        - **dataframe_id**: ID csv-файла(датафрейма)
    """
    return await DataframeService(user.id).move_prediction_to_active(model_id,
        dataframe_id)


@dataframes_methods_router.post("/feature_importances",
                                summary="Провести отбор признаков",
                                response_model=schemas.FeatureSelectionSummary)
async def feature_importances(dataframe_id: PydanticObjectId,
                            task_type: specs.FeatureSelectionTaskType,
                            selection_params: List[schemas.SelectorMethodParams],
                            user: User = Depends(current_active_user)):
    """
        Применяет методы отбора признаков к датафрейму. Возвращает таблицу результатов.
        На основе её, пользователь может выбрать какие признаки стоит удалять

        - **dataframe_id**: ID csv-файла(датафрейма)
        - **task_type**: тип задачи (классификация/регрессия)
        - **selection_params**: параметры для функции

        BaseSklearnModels для методов отбора:
        * 'linear_regression'
        * 'random_forest_regressor'
        * 'logistic_regression'
        * 'random_forest_classifier'

        Доступные методы:
        * 'variance_threshold': 'threshold' > 0
        * 'select_k_best': 'k'=1 > 1; 'score_func'
        * 'select_percentile': 1 < 'percentile'=10 < 100; 'score_func'
        * 'select_fpr': 0 < 'alpha'=0.05 < 1; 'score_func'
        * 'select_fdr': 0 < 'alpha'=0.05 < 1; 'score_func'
        * 'select_fwe': 0 < 'alpha'=0.05 < 1; 'score_func'
        * 'recursive_feature_elimination': 'n_features_to_select' > 1; 'step'=1 > 1; 'estimator'
        * 'sequential_forward_selection': 'n_features_to_select' > 1; 'estimator'
        * 'sequential_backward_selection': 'n_features_to_select' > 1; 'estimator'
        * 'select_from_model: 'estimator'

    """
    # await DataframeMetadataManagerService(user.id).get_dataframe_meta(dataframe_id)
    return await DataframeMethodsService(
        user.id).process_feature_importances(dataframe_id, task_type, selection_params)


@dataframes_methods_router.delete("/columns", summary="Удалить столбцы",
                                  response_model=models.DataFrameMetadata)
async def delete_column(dataframe_id: PydanticObjectId,
                        column_names: List[str],
                        user: User = Depends(current_active_user)):
    """
        Удаляет столбцы из датафрейма.
        *То же самое, что /apply_method?drop_columns*

        - **dataframe_id**: ID csv-файла(датафрейма)
        - **column_name**: имя столбца
    """
    method_params = schemas.ApplyMethodParams(
        method_name=specs.AvailableMethods.DROP_COLUMNS,
        columns=column_names
    )
    return await DataframeMethodsService(user.id).apply_changing_methods(
        dataframe_id, [method_params])


@dataframes_methods_router.put("/change_columns_type",
                               summary="Сменить тип столбца",
                               response_model=models.DataFrameMetadata)
async def change_column_type(dataframe_id: PydanticObjectId,
                             column_names: List[str],
                             new_type: specs.ColumnType,
                             user: User = Depends(current_active_user)):
    """
        Изменяет тип столбцов на заданный (числовой/категориальный).
        *То же самое, что /apply_method?change_columns_type*

        - **dataframe_id**: ID csv-файла(датафрейма)
        - **column_names**: имена столбцов
        - **new_type**: новый тип столбца (числовой/категориальный)
    """
    method_params = schemas.ApplyMethodParams(
        method_name=specs.AvailableMethods.CHANGE_COLUMNS_TYPE,
        columns=column_names,
        params={'new_type': new_type}
    )
    return await DataframeMethodsService(user.id).apply_change_columns_type(
        dataframe_id, [method_params])


@dataframes_methods_router.post("/apply_method",
                                response_model=models.DataFrameMetadata)
async def apply_method(dataframe_id: PydanticObjectId,
                       method_params: List[schemas.ApplyMethodParams],
                       user: User = Depends(current_active_user)):
    """
        Применяет метод обработки к датафрейму.

        - **dataframe_id**: ID csv-файла(датафрейма)
        - **method_params**: параметры для функций

        Доступные методы:
        - **drop_duplicates** - Remove duplicates
        - **drop_na** - Remove NA values
        - **drop_columns** - Remove columns

        - **fill_mean** - Replace NA values with the mean
        - **fill_median** - Replace NA values with the median
        - **fill_most_frequent** - Replace NA values with the most frequent value
        - **fill_custom_value** - Replace NA values with a custom value
        - **fill_bfill** - Fill NA values using backfill method
        - **fill_ffill** - Fill NA values using forward fill method
        - **fill_interpolation** - Fill NA values using interpolation
        - **fill_linear_imputer** - Replace NA values using a linear imputer
        - **fill_knn_imputer** - Replace NA values using a k-nearest neighbors imputer

        - **leave_n_values_encoding** - Leave N values encoding
        - **one_hot_encoding** - One-Hot encoding (OHE)
        - **ordinal_encoding** - Ordinal encoding

        - **standard_scaler** - Standardize numeric features
        - **min_max_scaler** - Scale features to a given range
        - **robust_scaler** - Scale features using statistics that are robust to outliers
    """
    return await DataframeMethodsService(user.id).apply_changing_methods(
        dataframe_id, method_params)

    # await DataframeMetadataManagerService(user.id).get_dataframe_meta(dataframe_id_from)
    # task = apply_function_celery.delay(str(user.id),
    #     str(dataframe_id), function_name.value, params)
    # return task.id


@dataframes_methods_router.post("/copy_pipeline",
                                response_model=models.DataFrameMetadata)
async def copy_pipeline(dataframe_id_from: PydanticObjectId,
                        dataframe_id_to: PydanticObjectId,
                        user: User = Depends(current_active_user)):
    """
        Применяет пайплайн от одного документа к другому.

        - **dataframe_id**: ID csv-файла(датафрейма) с которого копируется пайплайн
        - **dataframe_id**: ID csv-файла(датафрейма) на который применяется пайплайн
    """
    return await DataframeMethodsService(user.id).copy_pipeline(
        dataframe_id_from, dataframe_id_to)

    # await DataframeMetadataManagerService(user.id).get_dataframe_meta(dataframe_id_from)
    # await DataframeMetadataManagerService(user.id).get_dataframe_meta(dataframe_id_to)
    # task = copy_pipeline_celery.delay(str(user.id),
    #                                   dataframe_id_from, dataframe_id_to)
    # return task.id
