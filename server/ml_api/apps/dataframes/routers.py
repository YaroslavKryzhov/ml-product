from typing import List, Dict

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, UploadFile, File

from ml_api.apps.users.routers import current_active_user
from ml_api.apps.users.models import User
from ml_api.apps.dataframes.services.file_manager import DataframeFileManagerService
from ml_api.apps.dataframes.services.metadata_manager import DataframeMetadataManagerService
from ml_api.apps.dataframes.services.df_statistics_provider import DataframeStatisticsProviderService
from ml_api.apps.dataframes.services.dataframe_manager import DataframeManagerService
from ml_api.apps.dataframes.services.methods_manager import DataframeMethodsManagerService
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
    return await DataframeManagerService(user.id).upload_new_dataframe(
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
    return await DataframeFileManagerService(user.id).download_file(dataframe_id)


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
    return await DataframeMetadataManagerService(user.id).set_filename(
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
    return await DataframeFileManagerService(user.id).delete_file(dataframe_id)


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
    return await DataframeMetadataManagerService(user.id).get_dataframe_meta(dataframe_id)


@dataframes_metadata_router.get("/all", response_model=List[models.DataFrameMetadata],
    summary="Получить информацию обо всех csv-файлах (датафреймах)")
async def read_all_user_dataframes(user: User = Depends(current_active_user)):
    """
        Возвращает информацию обо всех датафреймах пользователя
    """
    return await DataframeMetadataManagerService(user.id).get_all_dataframes_meta()


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
    return await DataframeStatisticsProviderService(
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
    return await DataframeStatisticsProviderService(
        user.id).get_dataframe_column_statistics(dataframe_id)


@dataframes_content_router.get("/column_types",
                               response_model=models.ColumnTypes,
                               summary="Получить списки типов столбцов")
async def get_column_names(dataframe_id: PydanticObjectId,
                           user: User = Depends(current_active_user)):
    """
        Возвращает список имен столбцов датафрейма.

        - **dataframe_id**: ID csv-файла(датафрейма)
    """
    return await DataframeMetadataManagerService(
        user.id).get_column_types(dataframe_id)


@dataframes_content_router.get("/corr_matrix",
                               response_model=Dict[str, Dict[str, float]],
                               summary="Получить матрицу корреляций")
async def get_correlation_matrix(dataframe_id: PydanticObjectId,
                                 user: User = Depends(current_active_user)):
    """
        Возвращает матрицу корреляций для численных столбцов датафрейма.

        - **dataframe_id**: ID csv-файла(датафрейма)
    """
    return await DataframeStatisticsProviderService(
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
    return await DataframeMetadataManagerService(
        user.id).set_target_feature(dataframe_id, target_column)


@dataframes_methods_router.delete("/target",
                               summary="Очистить выбор целевого признака",
                               response_model=models.DataFrameMetadata)
async def set_target_feature(dataframe_id: PydanticObjectId,
                             user: User = Depends(current_active_user)):
    """
        Убирает отметку столбца датафрейма как целевого (Y).

        - **dataframe_id**: ID csv-файла(датафрейма)
    """
    return await DataframeMetadataManagerService(
        user.id).unset_target_feature(dataframe_id)


@dataframes_methods_router.put("/change_type",
                               summary="Сменить тип столбца",
                               response_model=models.DataFrameMetadata)
async def change_column_type(dataframe_id: PydanticObjectId,
                             column_name: str,
                             new_type: specs.ColumnType,
                             user: User = Depends(current_active_user)):
    """
        Изменяет тип столбца на заданный (числовой/категориальный).

        - **dataframe_id**: ID csv-файла(датафрейма)
        - **column_name**: имя численного столбца
        - **type**: тип столбца (числовой/категориальный)
    """
    return await DataframeManagerService(user.id
        ).convert_column_to_new_type(dataframe_id, column_name, new_type)


@dataframes_methods_router.put("/move_to_root",
                               summary="Переместить в корень интерфейса",
                               response_model=models.DataFrameMetadata)
async def move_to_root(dataframe_id: PydanticObjectId,
                             user: User = Depends(current_active_user)):
    """
        Переносит датафрейм из вложенного уровня в корень интерфейса.
        Либо переносит датафрейм из раздела предсказаний в корень интерфейса.

        - **dataframe_id**: ID csv-файла(датафрейма)
    """
    return await DataframeManagerService(user.id).move_dataframe_to_root(
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
        - **selection_params**: параметры для функции

        ScoreFunc для методов отбора:
        * 'chi2'
        * 'f_classif'
        * 'f_regression'

        BaseSklearnModels для методов отбора:
        * 'linear_regression'
        * 'random_forest_regressor'
        * 'logistic_regression'
        * 'linear_svc'
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
    return await DataframeMethodsManagerService(
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
    return await DataframeMethodsManagerService(user.id).apply_methods(
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
        * `drop_duplicates` - Remove duplicates
        * `drop_na` - Remove NA values
        * `drop_columns` - Remove columns

        * `fill_mean` - Replace NA values with the mean
        * `fill_median` - Replace NA values with the median
        * `fill_most_frequent` - Replace NA values with the most frequent value
        * `fill_custom_value` - Replace NA values with a custom value
        * `fill_bfill` - Fill NA values using backfill method
        * `fill_ffill` - Fill NA values using forward fill method
        * `fill_interpolation` - Fill NA values using interpolation
        * `fill_linear_imputer` - Replace NA values using a linear imputer
        * `fill_knn_imputer` - Replace NA values using a k-nearest neighbors imputer

        * `leave_n_values_encoding` - Leave N values encoding
        * `one_hot_encoding` - One-Hot encoding (OHE)
        * `ordinal_encoding` - Ordinal encoding

        * `standard_scaler` - Standardize numeric features
        * `min_max_scaler` - Scale features to a given range
        * `robust_scaler` - Scale features using statistics that are robust to outliers
    """
    return await DataframeMethodsManagerService(user.id).apply_methods(
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

        Обработка запускается ассинхронно в бэкграунд-режиме.
        Оповещение о конце процедуры обработки будет отправлено через Pub-Sub
        и будет получено пользователям, если он подключен к каналу по веб-сокету.

        В ответе возвращается ID бэкграунд-задачи и JWT для доступа к каналу.
        В случае возникновения ошибки в процессе - пайплайн не будет применен даже частично.
        В текущей реализации на датафрейм нельзя скопировать пайплайн, если у него уже есть свой пайплайн.

        - **dataframe_id**: ID csv-файла(датафрейма) с которого копируется пайплайн
        - **dataframe_id**: ID csv-файла(датафрейма) на который применяется пайплайн
    """
    return await DataframeMethodsManagerService(user.id).copy_pipeline(
        dataframe_id_from, dataframe_id_to)

    # await DataframeMetadataManagerService(user.id).get_dataframe_meta(dataframe_id_from)
    # await DataframeMetadataManagerService(user.id).get_dataframe_meta(dataframe_id_to)
    # task = copy_pipeline_celery.delay(str(user.id),
    #                                   dataframe_id_from, dataframe_id_to)
    # return task.id
