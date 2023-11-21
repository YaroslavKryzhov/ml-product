from typing import List

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.responses import JSONResponse

from ml_api import config
from ml_api.apps.users.routers import current_active_user
from ml_api.apps.users.model import User
from ml_api.apps.ml_models import schemas, specs, model
from ml_api.apps.ml_models.services.model_service import ModelService
from ml_api.apps.ml_models.services.fit_predict_service import ModelFitPredictService
from ml_api.apps.ml_models.services.jobs_manager import ModelJobsManager

models_file_router = APIRouter(
    prefix="/model",
    tags=["Models"],
    responses={404: {"description": "Not found"}},
)


@models_file_router.get("/download", summary="Скачать модель")
async def download_model(
    model_id: PydanticObjectId,
    user: User = Depends(current_active_user),
):
    """
        Скачивает модель.

        - **model_id**: ID модели
    """
    return await ModelService(user.id).download_model(model_id)


@models_file_router.put("/rename", summary="Переименовать модель",
                   response_model=model.ModelMetadata)
async def rename_model(
    model_id: PydanticObjectId,
    new_model_name: str,
    user: User = Depends(current_active_user),
):
    """
        Переименовывает модель.

        - **model_id**: ID модели
        - **new_model_name**: новое имя модели
    """
    return await ModelService(user.id).set_filename(
        model_id, new_model_name)


@models_file_router.delete("",  summary="Удалить модель",
                           response_model=model.ModelMetadata)
async def delete_model(
    model_id: PydanticObjectId,
    user: User = Depends(current_active_user),
):
    """
        Удаляет модель.

        - **model_id**: ID модели
    """
    return await ModelService(user.id).delete_model(model_id)


models_metadata_router = APIRouter(
    prefix="/model/metadata",
    tags=["Models Metadata"],
    responses={404: {"description": "Not found"}},
)


@models_metadata_router.get("", response_model=model.ModelMetadata,
    summary="Получить информацию о модели")
async def read_model_info(
    model_id: PydanticObjectId,
    user: User = Depends(current_active_user),
):
    """
        Возвращает информацию о модели.

        - **model_id**: ID модели
    """
    return await ModelService(user.id).get_model_meta(model_id)


@models_metadata_router.get("/all", response_model=List[model.ModelMetadata],
    summary="Получить информацию обо всех моделях пользователя")
async def read_all_user_models(user: User = Depends(current_active_user)):
    """
        Возвращает информацию обо всех моделях пользователя
    """
    return await ModelService(user.id).get_all_models_meta()


@models_metadata_router.get("/by_dataframe",
                            response_model=List[model.ModelMetadata],
    summary="Получить информацию обо всех моделях обученных на датафрейме")
async def read_all_user_models_by_dataframe(
        dataframe_id: PydanticObjectId,
        user: User = Depends(current_active_user)
):
    """
        Возвращает информацию обо всех моделях пользователя,
        обученных на данном датафрейме

        - **dataframe_id**: ID датафрейма
    """
    return await ModelService(
        user.id).get_all_models_meta_by_dataframe(dataframe_id=dataframe_id)


models_processing_router = APIRouter(
    prefix="/model/processing",
    tags=["Models Processing"],
    responses={404: {"description": "Not found"}},
)


@models_processing_router.post("/train")
async def train_model(model_name: str,
                dataframe_id: PydanticObjectId,
                task_type: specs.AvailableTaskTypes,
                model_params: schemas.ModelParams,
                params_type: specs.AvailableParamsTypes,
                background_tasks: BackgroundTasks,
                test_size: float = None,
                stratify: bool = None,
                user: User = Depends(current_active_user)):
    """
        Запускает обучение модели.

        - **model_name**: имя новой модели
        - **dataframe_id**: ID датафрейма
        - **task_type**: тип задачи
        - **model_params**: тип и гиперпараметры модели
        - **params_type**: тип подбора параметров (авто(hyperopt) только для
        классификации/регрессии/кластеризации)
        - **test_size**: размер валидационной выборки (классификация/регрессия)
        - **stratify**: делать ли стратификацию (при классификации)
    """
    model_meta = await ModelService(user.id).create_model(
        model_name=model_name,
        dataframe_id=dataframe_id,
        task_type=task_type,
        model_params=model_params,
        params_type=params_type,
        test_size=test_size,
        stratify=stratify)

    if config.RUN_ASYNC_TASKS:
        background_tasks.add_task(
            ModelJobsManager(user.id).train_model_async, model_meta)
        return JSONResponse(
            status_code=202,
            content={
                "message": "Задача принята и выполняется в фоновом режиме"}
        )
    else:
        return await ModelFitPredictService(
            user.id).train_model(model_meta=model_meta)


@models_processing_router.post("/build_composition")
async def build_composition(composition_name: str,
                      model_ids: List[PydanticObjectId],
                      composition_params: schemas.ModelParams,
                background_tasks: BackgroundTasks,
                user: User = Depends(current_active_user)):
    composition_meta = await ModelService(user.id).create_composition(
        composition_name=composition_name, model_ids=model_ids,
        composition_params=composition_params)

    if config.RUN_ASYNC_TASKS:
        background_tasks.add_task(
            ModelJobsManager(user.id).build_composition_async, composition_meta)
        return JSONResponse(
            status_code=202,
            content={
                "message": "Задача принята и выполняется в фоновом режиме"}
        )
    else:
        return await ModelFitPredictService(
            user.id).train_composition(composition_meta=composition_meta)


@models_processing_router.put("/predict")
async def predict_on_model(dataframe_id: PydanticObjectId,
            model_id: PydanticObjectId,
            prediction_name: str,
            background_tasks: BackgroundTasks,
            apply_pipeline: bool = True,
            user: User = Depends(current_active_user)):
    """
        Делает предсказание на модели.

        - **dataframe_id**: ID датафрейма
        - **model_id**: ID модели
        - **apply_pipeline**: применять ли пайплайн с выборки, на которой
        училась модель

        Если данные в сыром виде, можно скопировать пайплайн с
        оригинальной выборки перед предсказанием.
        Если данные уже предобработаны, можно поставить параметр = False.
    """
    if config.RUN_ASYNC_TASKS:
        await ModelService(user.id).get_model_meta(model_id)
        await ModelFitPredictService(user.id).check_prediction_params(
            dataframe_id, prediction_name)
        background_tasks.add_task(
            ModelJobsManager(user.id).predict_on_model_async,
            dataframe_id, model_id, prediction_name, apply_pipeline)
        return JSONResponse(
            status_code=202,
            content={
                "message": "Задача принята и выполняется в фоновом режиме"}
        )
    else:
        return await ModelFitPredictService(user.id).predict_on_model(
            source_df_id=dataframe_id,
            model_id=model_id,
            prediction_name=prediction_name,
            apply_pipeline=apply_pipeline)


models_specs_router = APIRouter(
    prefix="/model/specs",
    tags=["Models Specs"],
    responses={404: {"description": "Not found"}},
)


@models_specs_router.get("/task_types")
def get_available_task_types():
    return [task.value for task in specs.AvailableTaskTypes]


@models_specs_router.get("/params_types")
def get_available_params_types():
    return [param.value for param in specs.AvailableParamsTypes]


@models_specs_router.get("/model_statuses")
def get_model_statuses():
    return [status.value for status in specs.ModelStatuses]


@models_specs_router.get("/model_types")
def get_available_model_types():
    return [model.value for model in specs.AvailableModelTypes]


@models_specs_router.get("/model_types/parameters/{model_type}")
def get_parameters_for_model_type(model_type: specs.AvailableModelTypes):
    from ml_api.apps.ml_models.models_specs.validation_params import (
        classification_models_params,
        regression_models_params,
        clustering_models_params,
        dimensionality_reduction_models_params,
        outlier_detection_models_params,
        classification_compositions_params,
        regression_compositions_params
    )
    # Classification models
    if model_type == specs.AvailableModelTypes.DECISION_TREE_CLASSIFIER:
           return classification_models_params.DecisionTreeClassifierParams.schema()
    if model_type == specs.AvailableModelTypes.DECISION_TREE_CLASSIFIER:
        return classification_models_params.DecisionTreeClassifierParams.schema()
    elif model_type == specs.AvailableModelTypes.RANDOM_FOREST_CLASSIFIER:
        return classification_models_params.RandomForestClassifierParams.schema()
    elif model_type == specs.AvailableModelTypes.EXTRA_TREES_CLASSIFIER:
        return classification_models_params.ExtraTreesClassifierParams.schema()
    elif model_type == specs.AvailableModelTypes.GRADIENT_BOOSTING_CLASSIFIER:
        return classification_models_params.GradientBoostingClassifierParams.schema()
    elif model_type == specs.AvailableModelTypes.ADABOOST_CLASSIFIER:
        return classification_models_params.AdaBoostClassifierParams.schema()
    elif model_type == specs.AvailableModelTypes.BAGGING_CLASSIFIER:
        return classification_models_params.BaggingClassifierParams.schema()
    elif model_type == specs.AvailableModelTypes.XGB_CLASSIFIER:
        return classification_models_params.XGBClassifierParams.schema()
    elif model_type == specs.AvailableModelTypes.LGBM_CLASSIFIER:
        return classification_models_params.LGBMClassifierParams.schema()
    elif model_type == specs.AvailableModelTypes.CATBOOST_CLASSIFIER:
        return classification_models_params.CatBoostClassifierParams.schema()
    elif model_type == specs.AvailableModelTypes.SGD_CLASSIFIER:
        return classification_models_params.SGDClassifierParams.schema()
    elif model_type == specs.AvailableModelTypes.LINEAR_SVC:
        return classification_models_params.LinearSVCParams.schema()
    elif model_type == specs.AvailableModelTypes.SVC:
        return classification_models_params.SVCParams.schema()
    elif model_type == specs.AvailableModelTypes.LOGISTIC_REGRESSION:
        return classification_models_params.LogisticRegressionParams.schema()
    elif model_type == specs.AvailableModelTypes.PASSIVE_AGGRESSIVE_CLASSIFIER:
        return classification_models_params.PassiveAggressiveClassifierParams.schema()
    elif model_type == specs.AvailableModelTypes.KNEIGHBORS_CLASSIFIER:
        return classification_models_params.KNeighborsClassifierParams.schema()
    elif model_type == specs.AvailableModelTypes.RADIUS_NEIGHBORS_CLASSIFIER:
        return classification_models_params.RadiusNeighborsClassifierParams.schema()
    elif model_type == specs.AvailableModelTypes.MLP_CLASSIFIER:
        return classification_models_params.MLPClassifierParams.schema()

    # Regression models
    elif model_type == specs.AvailableModelTypes.DECISION_TREE_REGRESSOR:
        return regression_models_params.DecisionTreeRegressorParams.schema()
    elif model_type == specs.AvailableModelTypes.RANDOM_FOREST_REGRESSOR:
        return regression_models_params.RandomForestRegressorParams.schema()
    elif model_type == specs.AvailableModelTypes.EXTRA_TREES_REGRESSOR:
        return regression_models_params.ExtraTreesRegressorParams.schema()
    elif model_type == specs.AvailableModelTypes.GRADIENT_BOOSTING_REGRESSOR:
        return regression_models_params.GradientBoostingRegressorParams.schema()
    elif model_type == specs.AvailableModelTypes.ADABOOST_REGRESSOR:
        return regression_models_params.AdaBoostRegressorParams.schema()
    elif model_type == specs.AvailableModelTypes.BAGGING_REGRESSOR:
        return regression_models_params.BaggingRegressorParams.schema()
    elif model_type == specs.AvailableModelTypes.XGB_REGRESSOR:
        return regression_models_params.XGBRegressorParams.schema()
    elif model_type == specs.AvailableModelTypes.LGBM_REGRESSOR:
        return regression_models_params.LGBMRegressorParams.schema()
    elif model_type == specs.AvailableModelTypes.CATBOOST_REGRESSOR:
        return regression_models_params.CatBoostRegressorParams.schema()
    elif model_type == specs.AvailableModelTypes.SGD_REGRESSOR:
        return regression_models_params.SGDRegressorParams.schema()
    elif model_type == specs.AvailableModelTypes.LINEAR_SVR:
        return regression_models_params.LinearSVRParams.schema()
    elif model_type == specs.AvailableModelTypes.SVR:
        return regression_models_params.SVRParams.schema()
    elif model_type == specs.AvailableModelTypes.LINEAR_REGRESSION:
        return regression_models_params.LinearRegressionParams.schema()
    elif model_type == specs.AvailableModelTypes.RIDGE:
        return regression_models_params.RidgeParams.schema()
    elif model_type == specs.AvailableModelTypes.LASSO:
        return regression_models_params.LassoParams.schema()
    elif model_type == specs.AvailableModelTypes.ELASTIC_NET:
        return regression_models_params.ElasticNetParams.schema()
    elif model_type == specs.AvailableModelTypes.PASSIVE_AGGRESSIVE_REGRESSOR:
        return regression_models_params.PassiveAggressiveRegressorParams.schema()
    elif model_type == specs.AvailableModelTypes.K_NEIGHBORS_REGRESSOR:
        return regression_models_params.KNeighborsRegressorParams.schema()
    elif model_type == specs.AvailableModelTypes.RADIUS_NEIGHBORS_REGRESSOR:
        return regression_models_params.RadiusNeighborsRegressorParams.schema()
    elif model_type == specs.AvailableModelTypes.MLP_REGRESSOR:
        return regression_models_params.MLPRegressorParams.schema()

    # Clustering models
    elif model_type == specs.AvailableModelTypes.KMEANS:
        return clustering_models_params.KMeansParams.schema()
    elif model_type == specs.AvailableModelTypes.MINI_BATCH_KMEANS:
        return clustering_models_params.MiniBatchKMeansParams.schema()
    elif model_type == specs.AvailableModelTypes.AFFINITY_PROPAGATION:
        return clustering_models_params.AffinityPropagationParams.schema()
    elif model_type == specs.AvailableModelTypes.MEAN_SHIFT:
        return clustering_models_params.MeanShiftParams.schema()
    elif model_type == specs.AvailableModelTypes.SPECTRAL_CLUSTERING:
        return clustering_models_params.SpectralClusteringParams.schema()
    elif model_type == specs.AvailableModelTypes.WARD:
        return clustering_models_params.WardParams.schema()
    elif model_type == specs.AvailableModelTypes.AGGLOMERATIVE_CLUSTERING:
        return clustering_models_params.AgglomerativeClusteringParams.schema()
    elif model_type == specs.AvailableModelTypes.DBSCAN:
        return clustering_models_params.DBSCANParams.schema()
    elif model_type == specs.AvailableModelTypes.OPTICS:
        return clustering_models_params.OPTICSParams.schema()
    elif model_type == specs.AvailableModelTypes.BIRCH:
        return clustering_models_params.BirchParams.schema()
    elif model_type == specs.AvailableModelTypes.GAUSSIAN_MIXTURE:
        return clustering_models_params.GaussianMixtureParams.schema()

    # Outlier detection models
    elif model_type == specs.AvailableModelTypes.ONE_CLASS_SVM:
        return outlier_detection_models_params.OneClassSVMParams.schema()
    elif model_type == specs.AvailableModelTypes.SGD_ONE_CLASS_SVM:
        return outlier_detection_models_params.SGDOneClassSVMParams.schema()
    elif model_type == specs.AvailableModelTypes.ELLIPTIC_ENVELOPE:
        return outlier_detection_models_params.EllipticEnvelopeParams.schema()
    elif model_type == specs.AvailableModelTypes.LOCAL_OUTLIER_FACTOR:
        return outlier_detection_models_params.LocalOutlierFactorParams.schema()
    elif model_type == specs.AvailableModelTypes.ISOLATION_FOREST:
        return outlier_detection_models_params.IsolationForestParams.schema()

    # Dimensionality reduction models
    elif model_type == specs.AvailableModelTypes.PCA:
        return dimensionality_reduction_models_params.PCAParams.schema()
    elif model_type == specs.AvailableModelTypes.LINEAR_DISCRIMINANT_ANALYSIS:
        return dimensionality_reduction_models_params.LinearDiscriminantAnalysisParams.schema()
    elif model_type == specs.AvailableModelTypes.TSNE:
        return dimensionality_reduction_models_params.TSNEParams.schema()
    elif model_type == specs.AvailableModelTypes.ISOMAP:
        return dimensionality_reduction_models_params.IsomapParams.schema()
    elif model_type == specs.AvailableModelTypes.NMF:
        return dimensionality_reduction_models_params.NMFParams.schema()
    elif model_type == specs.AvailableModelTypes.TRUNCATED_SVD:
        return dimensionality_reduction_models_params.TruncatedSVDParams.schema()

    # Classification composition models
    elif model_type == specs.AvailableModelTypes.VOTING_CLASSIFIER:
        return classification_compositions_params.VotingClassifierParams.schema()
    elif model_type == specs.AvailableModelTypes.STACKING_CLASSIFIER:
        return classification_compositions_params.StackingClassifierParams.schema()

    # Regression composition models
    elif model_type == specs.AvailableModelTypes.VOTING_REGRESSOR:
        return regression_compositions_params.VotingRegressorParams.schema()
    elif model_type == specs.AvailableModelTypes.STACKING_REGRESSOR:
        return regression_compositions_params.StackingRegressorParams.schema()

    else:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Unrecognized model type: '{model_type}'."
        )


