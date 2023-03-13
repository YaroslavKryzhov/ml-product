from typing import List, Any
from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile, File, status, Response

from ml_api.common.dependencies.db_deps import get_db
from ml_api.apps.users.routers import current_active_user
from ml_api.apps.users.models import User
from ml_api.apps.dataframes.services.services import DataframeManagerService
from ml_api.apps.dataframes import schemas, specs
from ml_api.common.celery_tasks.celery_tasks import apply_function_celery, \
    copy_pipeline_celery
from ml_api.common.celery_tasks.schemas import TaskJwtResponse
from ml_api.common.security.token_utils import create_centrifugo_token

dataframes_file_router = APIRouter(
    prefix="/dataframe",
    tags=["Dataframe As File"],
    responses={404: {"description": "Not found"}},
)


@dataframes_file_router.post("", summary="Загрузить csv-файл")
def upload_dataframe(
    filename: str,
    file: UploadFile = File(...),
    db: get_db = Depends(),
    user: User = Depends(current_active_user),
):
    """
        Загружает файл в систему

        - **filename**: сохраняемое имя файла
        - **file**: csv-файл
    """
    dataframe_id = DataframeManagerService(db, user.id).upload_file(
        file=file.file, filename=filename
    )
    return Response(
        status_code=status.HTTP_200_OK,
        content=dataframe_id,
        media_type='text/plain',
    )


@dataframes_file_router.get("/download", summary="Скачать csv-файл",
                            response_description="FileResponse")
def download_dataframe(
    dataframe_id: UUID,
    db: get_db = Depends(),
    user: User = Depends(current_active_user),
):
    """
        Скачивает csv-файл пользователя

        - **dataframe_id**: ID csv-файла(датафрейма)
    """
    result = DataframeManagerService(db, user.id).download_file(dataframe_id)
    return result


@dataframes_file_router.put("/rename", summary="Переименовать csv-файл")
def rename_dataframe(
    dataframe_id: UUID,
    new_filename: str,
    db: get_db = Depends(),
    user: User = Depends(current_active_user),
):
    """
        Переименовывает csv-файл

        - **dataframe_id**: ID csv-файла(датафрейма)
        - **new_filename**: новое имя файла
    """
    DataframeManagerService(db, user.id).rename_file(
        dataframe_id, new_filename
    )
    return Response(
        status_code=status.HTTP_200_OK,
        content=f"Document with id {dataframe_id} successfully renamed to '{new_filename}'.",
        media_type='text/plain',
    )


@dataframes_file_router.delete("", summary="Удалить csv-файл")
def delete_dataframe(
    dataframe_id: UUID,
    db: get_db = Depends(),
    user: User = Depends(current_active_user),
):
    """
        Удаляет csv-файл

        - **dataframe_id**: ID csv-файла(датафрейма)
    """
    DataframeManagerService(db, user.id).delete_file(dataframe_id)
    return Response(
        status_code=status.HTTP_200_OK,
        content=str(dataframe_id),
        media_type='text/plain',
    )


@dataframes_file_router.get("", response_model=schemas.DataFrameInfo,
    summary="Получить информацию о csv-файле (датафрейме)",
    response_description="DataFrameInfo json-объект")
def read_dataframe_info(
    dataframe_id: UUID,
    db: get_db = Depends(),
    user: User = Depends(current_active_user),
):
    """
        Возвращает информацию о датафрейме

        - **dataframe_id**: ID csv-файла(датафрейма)
    """
    return DataframeManagerService(db, user.id
        ).get_dataframe_info(dataframe_id)


@dataframes_file_router.get("/all", response_model=List[schemas.DataFrameInfo],
    summary="Получить информацию обо всех csv-файлах (датафреймах)",
    response_description="Массив DataFrameInfo json-объектов"
)
def read_all_user_dataframes(
    db: get_db = Depends(), user: User = Depends(current_active_user)
):
    """
        Возвращает информацию обо всех датафреймах пользователя
    """
    return DataframeManagerService(db, user.id).get_all_dataframes_info()


dataframes_df_router = APIRouter(
    prefix="/dataframe/df",
    tags=["Dataframe As pandas.DataFrame"],
    responses={404: {"description": "Not found"}},
)


@dataframes_df_router.get("", response_model=schemas.ReadDataFrameResponse,
    summary="Прочитать датафрейм",
    response_description="Всего страниц, содержимое страницы")
def read_dataframe_with_pagination(
    dataframe_id: UUID,
    page: int = 1,
    rows_on_page: int = 50,
    db: get_db = Depends(),
    user: User = Depends(current_active_user),
):
    """
        Возвращает содержимое csv-файла (датафрейма) с пагинацией

        - **dataframe_id**: ID csv-файла(датафрейма)
        - **page**: номер cтраницы (default=1)
        - **rows_on_page**: кол-во строк датафрейма на cтраницу (default=1)
    """
    return DataframeManagerService(db, user.id
        ).get_dataframe_with_pagination(dataframe_id, page, rows_on_page)


@dataframes_df_router.get("/columns", response_model=List[str],
                          summary="Получить список столбцов",
                          response_description="Массив имен стоблцов"
)
def get_column_names(
    dataframe_id: UUID,
    db: get_db = Depends(),
    user: User = Depends(current_active_user),
):
    """
        Возвращает список имен столбцов датафрейма.

        - **dataframe_id**: ID csv-файла(датафрейма)
    """
    return DataframeManagerService(db, user.id
        ).get_dataframe_columns(dataframe_id)


@dataframes_df_router.get("/statistics",
    response_model=List[schemas.ColumnDescription],
    summary="Получить описание столбцов",
    response_description="Массив стоблцов с их характеристиками")
def dataframe_columns_stat_info(
    dataframe_id: UUID,
    db: get_db = Depends(),
    user: User = Depends(current_active_user),
):
    """
        Возвращает описание для всех столбцов датафрейма:

        * Имя столбца
        * Тип (численный, категориальный)
        * Количество непустых значений
        * Тип данных (int, float64, object, etc.)
        * Содержание:
            * для численных – гистограмма распределения (pandas.hist())
            * для категориальных – количество значений (pandas.value_counts())

        - **dataframe_id**: ID csv-файла(датафрейма)
    """
    return DataframeManagerService(db, user.id
        ).get_dataframe_column_statistics(dataframe_id)


@dataframes_df_router.get("/describe",
    response_model=schemas.DataFrameDescription,
    summary="Получить статистическое описание данных",
    response_description="Массив численных стоблцов с их характеристиками")
def dataframe_stat_describe(
    dataframe_id: UUID,
    db: get_db = Depends(),
    user: User = Depends(current_active_user),
):
    """
        Возвращает статистическое описание численных столбцов датафрейма.

        Аналогично методу **pandas.describe()**

        - **dataframe_id**: ID csv-файла(датафрейма)
    """
    return DataframeManagerService(db, user.id
        ).get_dataframe_statistic_description(dataframe_id)


dataframes_method_router = APIRouter(
    prefix="/dataframe/edit",
    tags=["Dataframe Editions"],
    responses={404: {"description": "Not found"}},
)


@dataframes_method_router.put("/target",
    summary="Задать целевой признак")
def set_target_feature(
    dataframe_id: UUID,
    target_column: str,
    db: get_db = Depends(),
    user: User = Depends(current_active_user),
):
    """
        Помечает столбец датафрейма как целевой (Y).

        - **dataframe_id**: ID csv-файла(датафрейма)
        - **target_column**: имя целевого столбца
    """
    DataframeManagerService(db, user.id).set_target_column(
        dataframe_id, target_column)

    return Response(
        status_code=status.HTTP_200_OK,
        content=f"The column '{target_column}' is set as target.",
        media_type='text/plain',
    )


@dataframes_method_router.put("/to_categorical",
    summary="Сменить тип столбца на категориальный")
def set_column_as_categorical(
    dataframe_id: UUID,
    column_name: str,
    db: get_db = Depends(),
    user: User = Depends(current_active_user),
):
    """
        Изменяет тип численного столбца на категориальный.

        - **dataframe_id**: ID csv-файла(датафрейма)
        - **column_name**: имя численного столбца
    """
    DataframeManagerService(db, user.id
        ).change_column_type_to_categorical(dataframe_id, column_name)
    return Response(
        status_code=status.HTTP_200_OK,
        content=f"The column '{column_name}' is set as categorical",
        media_type='text/plain',
    )


@dataframes_method_router.put("/to_numeric",
    summary="Сменить тип столбца на численный")
def set_column_as_numeric(
    dataframe_id: UUID,
    column_name: str,
    db: get_db = Depends(),
    user: User = Depends(current_active_user),
):
    """
        Изменяет тип категориального столбца на численный.

        - **dataframe_id**: ID csv-файла(датафрейма)
        - **column_name**: имя категориального столбца
    """
    DataframeManagerService(db, user.id
        ).change_column_type_to_numeric(dataframe_id, column_name)
    return Response(
        status_code=status.HTTP_200_OK,
        content=f"The column '{column_name}' is set as numeric",
        media_type='text/plain',
    )


@dataframes_method_router.delete("/column", summary="Удалить столбец")
def delete_column(
    dataframe_id: UUID,
    column_name: str,
    db: get_db = Depends(),
    user: User = Depends(current_active_user),
):
    """
        Удаляет столбец из датафрейма.
        *То же самое, что /apply_method?function_name="drop_column"*

        - **dataframe_id**: ID csv-файла(датафрейма)
        - **column_name**: имя столбца
    """
    DataframeManagerService(db, user.id).get_dataframe_info(dataframe_id)

    DataframeManagerService(db, user.id).apply_function(
        dataframe_id, specs.AvailableFunctions.drop_column, column_name
    )
    return Response(
        status_code=status.HTTP_200_OK,
        content=f"The column '{column_name}' successfully deleted",
        media_type='text/plain',
    )


@dataframes_method_router.post("/apply_method", response_model=TaskJwtResponse)
def apply_method(
    dataframe_id: UUID,
    function_name: specs.AvailableFunctions,
    params: Any = None,
    db: get_db = Depends(),
    user: User = Depends(current_active_user),
):
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
    DataframeManagerService(db, user.id).get_dataframe_info(dataframe_id)

    # DataframeManagerService(db, user.id).apply_function(dataframe_id,
    #                                         function_name.value, params)
    task = apply_function_celery.delay(str(user.id),
        str(dataframe_id), function_name.value, params)
    jwt_token = create_centrifugo_token(str(user.id))
    return TaskJwtResponse(
        task_id=task.id,
        jwt_token=jwt_token,
    )


@dataframes_method_router.post("/copy_pipeline", response_model=TaskJwtResponse)
def copy_pipeline(
    dataframe_id_from: UUID,
    dataframe_id_to: UUID,
    db: get_db = Depends(),
    user: User = Depends(current_active_user),
):
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
    DataframeManagerService(db, user.id).get_dataframe_info(dataframe_id_from)
    DataframeManagerService(db, user.id).get_dataframe_info(dataframe_id_to)

    # DataframeManagerService(db, user.id).copy_pipeline(dataframe_id_from, dataframe_id_to)
    task = copy_pipeline_celery.delay(str(user.id),
                                      dataframe_id_from, dataframe_id_to)
    jwt_token = create_centrifugo_token(str(user.id))
    return TaskJwtResponse(
        task_id=task.id,
        jwt_token=jwt_token,
    )
