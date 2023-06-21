from typing import List, Dict, Any

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, UploadFile, File, status
from fastapi.responses import Response

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
    return await DataframeManagerService(user.id).add_dataframe(
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
    return await DataframeMetadataManagerService(user.id).set_filename(dataframe_id, new_filename)


@dataframes_file_router.delete("", summary="Удалить csv-файл")
async def delete_dataframe(
    dataframe_id: PydanticObjectId,
    user: User = Depends(current_active_user),
):
    """
        Удаляет csv-файл

        - **dataframe_id**: ID csv-файла(датафрейма)
    """
    await DataframeFileManagerService(user.id).delete_file(dataframe_id)
    return Response(
        status_code=status.HTTP_200_OK,
        content=f"Dataframe with id '{dataframe_id}' deleted",
        media_type='text/plain',
    )


dataframes_metadata_router = APIRouter(
    prefix="/dataframe/metadata",
    tags=["Dataframe Metadata"],
    responses={404: {"description": "Not found"}},
)


@dataframes_metadata_router.get("", response_model=models.DataFrameMetadata,
    summary="Получить информацию о csv-файле (датафрейме)",
    response_description="DataFrameMetadata json-объект")
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
    summary="Получить информацию обо всех csv-файлах (датафреймах)",
    response_description="Массив DataFrameMetadata json-объектов")
async def read_all_user_dataframes(user: User = Depends(current_active_user)):
    """
        Возвращает информацию обо всех датафреймах пользователя
    """
    return await DataframeMetadataManagerService(user.id).get_all_dataframes_meta()


dataframes_content_router = APIRouter(
    prefix="/dataframe/content",
    tags=["Dataframe Content"],
    responses={404: {"description": "Not found"}})


@dataframes_content_router.get("", response_model=schemas.ReadDataFrameResponse,
    summary="Прочитать датафрейм",
    response_description="Всего страниц, содержимое страницы")
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
    return await DataframeStatisticsProviderService(user.id).get_dataframe_with_pagination(dataframe_id, page, rows_on_page)


@dataframes_content_router.get("/statistics",
    response_model=List[schemas.ColumnDescription],
    summary="Получить описание столбцов",
    response_description="Массив стоблцов с их характеристиками")
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
    return await DataframeStatisticsProviderService(user.id).get_dataframe_column_statistics(dataframe_id)


@dataframes_content_router.get("/column_types", response_model=models.ColumnTypes,
                          summary="Получить списки типов столбцов",
                          response_description="Списки категориальных и численных столбцов")
async def get_column_names(dataframe_id: PydanticObjectId, user: User = Depends(current_active_user)):
    """
        Возвращает список имен столбцов датафрейма.

        - **dataframe_id**: ID csv-файла(датафрейма)
    """
    return await DataframeMetadataManagerService(user.id).get_column_types(dataframe_id)


@dataframes_content_router.get("/corr_matrix", response_model=Dict[str, Dict[str, float]],
                          summary="Получить матрицу корреляций",
                          response_description="Словарь словарей")
async def get_correlation_matrix(dataframe_id: PydanticObjectId, user: User = Depends(current_active_user)):
    """
        Возвращает матрицу корреляций для численных столбцов датафрейма.

        - **dataframe_id**: ID csv-файла(датафрейма)
    """
    return await DataframeStatisticsProviderService(user.id).get_correlation_matrix(dataframe_id)


dataframes_methods_router = APIRouter(
    prefix="/dataframe/edit",
    tags=["Dataframe Editions"],
    responses={404: {"description": "Not found"}},
)


@dataframes_methods_router.put("/target",
                               summary="Задать целевой признак")
async def set_target_feature(dataframe_id: PydanticObjectId, target_column: str,
                       user: User = Depends(current_active_user)):
    """
        Помечает столбец датафрейма как целевой (Y).

        - **dataframe_id**: ID csv-файла(датафрейма)
        - **target_column**: имя целевого столбца
    """
    await DataframeMetadataManagerService(user.id).set_target_feature(dataframe_id, target_column)
    return Response(
        status_code=status.HTTP_200_OK,
        content=f"The column '{target_column}' is set as target.",
        media_type='text/plain',
    )


@dataframes_methods_router.put("/change_type",
                               summary="Сменить тип столбца")
async def set_column_as_categorical(dataframe_id: PydanticObjectId, column_name: str,
                                    new_type: specs.ColumnType,
                                    user: User = Depends(current_active_user)):
    """
        Изменяет тип столбца на заданный (числовой/категориальный).

        - **dataframe_id**: ID csv-файла(датафрейма)
        - **column_name**: имя численного столбца
        - **type**: тип столбца (числовой/категориальный)
    """
    await DataframeManagerService(user.id
        ).convert_column_to_new_type(dataframe_id, column_name, new_type)
    return Response(
        status_code=status.HTTP_200_OK,
        content=f"Changed type of column '{column_name}' to '{new_type}'.",
        media_type='text/plain',
    )


@dataframes_methods_router.delete("/column", summary="Удалить столбец")
async def delete_column(dataframe_id: PydanticObjectId, column_name: str,
                  user: User = Depends(current_active_user)):
    """
        Удаляет столбец из датафрейма.
        *То же самое, что /apply_method?function_name="drop_column"*

        - **dataframe_id**: ID csv-файла(датафрейма)
        - **column_name**: имя столбца
    """
    await DataframeMetadataManagerService(user.id).get_dataframe_meta(dataframe_id)
    await DataframeMethodsManagerService(user.id).apply_function(
        dataframe_id, specs.AvailableFunctions.drop_column, column_name)
    return Response(
        status_code=status.HTTP_200_OK,
        content=f"The column '{column_name}' successfully deleted",
        media_type='text/plain',
    )


@dataframes_methods_router.post("/apply_method")
async def apply_method(dataframe_id: PydanticObjectId, function_name: specs.AvailableFunctions,
                 params: Any = None, user: User = Depends(current_active_user)):
    """
        Применяет метод обработки к датафрейму.

        Обработка запускается ассинхронно в бэкграунд-режиме.
        Оповещение о конце процедуры обработки будет отправлено через Pub-Sub
        и будет получено пользователям, если он подключен к каналу по веб-сокету.

        В ответе возвращается ID бэкграунд-задачи и JWT для доступа к каналу.

        - **dataframe_id**: ID csv-файла(датафрейма)
        - **function_name**: имя выбранной функции
        - **params**: параметры для функции (в текущей реализации нужны только для 'drop_column')

        Доступные методы:
        * 'remove_duplicates' – Удаление дубликатов
        * 'drop_na' – Удаление пропусков
        * 'drop_column' – Удаление столбца
        * 'miss_insert_mean_mode' – Замена пропусков: Среднее и мода
        * 'miss_linear_imputer' – Замена пропусков: Линейная модель
        * 'miss_knn_imputer' – Замена пропусков: К-ближних соседей
        * 'standardize_features' – Стандартизация цисленных признаков
        * 'ordinal_encoding' – Порядковое кодирование
        * 'one_hot_encoding' – One-Hot кодирование (OHE)
        * 'outliers_isolation_forest' – Удаление выбросов: IsolationForest
        * 'outliers_elliptic_envelope' – Удаление выбросов: EllipticEnvelope
        * 'outliers_local_factor' – Удаление выбросов: LocalOutlierFactor
        * 'outliers_one_class_svm' – Удаление выбросов: OneClassSVM
        * 'outliers_sgd_one_class_svm' – Удаление выбросов: SGDOneClassSVM

    """
    await DataframeMetadataManagerService(user.id).get_dataframe_meta(dataframe_id)
    await DataframeMethodsManagerService(user.id).apply_function(dataframe_id,
                                            function_name.value, params)
    return Response(
        status_code=status.HTTP_200_OK,
        content=f"Method '{function_name}' successfully applied",
        media_type='text/plain',
    )
    # task = apply_function_celery.delay(str(user.id),
    #     str(dataframe_id), function_name.value, params)
    # return task.id


@dataframes_methods_router.post("/copy_pipeline")
async def copy_pipeline(dataframe_id_from: PydanticObjectId, dataframe_id_to: PydanticObjectId,
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
    await DataframeMetadataManagerService(user.id).get_dataframe_meta(dataframe_id_from)
    await DataframeMetadataManagerService(user.id).get_dataframe_meta(dataframe_id_to)
    await DataframeMethodsManagerService(user.id).copy_pipeline(dataframe_id_from, dataframe_id_to)
    return Response(
        status_code=status.HTTP_200_OK,
        content=f"Pipeline successfully applied",
        media_type='text/plain',
    )
    # task = copy_pipeline_celery.delay(str(user.id),
    #                                   dataframe_id_from, dataframe_id_to)
    # return task.id
