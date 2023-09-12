from ml_api.apps.ml_models.services.model_construstor import ModelConstructorService
from ml_api.apps.ml_models.services.model_trainer import ModelTrainerService
from ml_api.apps.ml_models.services.params_validator import ParamsValidationService
from ml_api.apps.ml_models.services.metadata_manager import ModelMetadataManagerService
from ml_api.apps.ml_models.services.file_manager import ModelFileManagerService
from ml_api.apps.ml_models import specs, schemas
from ml_api.apps.ml_models.models import ModelMetadata


class ModelProcessingManagerService:
    """
    Отвечает за обработку запросов на обучение и предсказание моделей.
    """
    def __init__(self, user_id):
        self._user_id = user_id
        self.file_manager = ModelFileManagerService(self._user_id)
        self.metadata_manager = ModelMetadataManagerService(self._user_id)

    async def _set_problem_status(self, model_id):
        await self.metadata_manager.set_status(
            model_id, specs.ModelStatuses.PROBLEM)

    async def prepare_model(self, model_meta: ModelMetadata):  # -> sklearn.Estimator
        """
        Валидирует параметры модели и создает её экземпляр.
        """
        dataframe_info = schemas.DataframeGetterInfo(
            dataframe_id=model_meta.dataframe_id,
            user_id=self._user_id
        )
        model_params = model_meta.model_params
        params_type = model_meta.params_type
        task_type = model_meta.task_type

        try:
            model_params_validated = await ParamsValidationService().validate_params(
                task_type, model_params, params_type, dataframe_info)
        except Exception as err:
            await self._set_problem_status(model_meta.id)
            raise err

        await self.metadata_manager.set_model_params(
            model_meta.id, model_params_validated)

        try:
            model = ModelConstructorService().get_model(task_type,
                                                        model_params_validated)
        except Exception as err:
            await self._set_problem_status(model_meta.id)
            raise err

        return model

    def train_model(self, model_meta: ModelMetadata, model):
        """
        Обучает предоставленную модель на данных из датафрейма.
        """
        model_id = model_meta.id
        self.metadata_manager.set_status(model_id, specs.ModelStatuses.TRAINING)
        try:
            model, metrics = ModelTrainerService(model_meta, model).train_model()
        except Exception as e:
            await self._set_problem_status(model_id)
            raise e
        self.metadata_manager.set_status(model_id, specs.ModelStatuses.TRAINED)

        try:
            self.file_manager.save_model(model_id, model)
        except Exception as e:
            await self._set_problem_status(model_id)
            raise e

    # def predict_on_model(self, dataframe_id: UUID, model_id: UUID):
    #     features = DataframeManagerService(self._db, self._user_id
    #         ).get_feature_df(dataframe_id=dataframe_id)
    #     model_info = ModelInfoCRUD(self._db, self._user_id).get(model_id)
    #     if features.columns.to_list() != model_info.features:
    #         return JSONResponse(
    #             status_code=status.HTTP_406_NOT_ACCEPTABLE,
    #             content="Features in doc and in model training history are "
    #                     "different",
    #         )
    #     if model_info.save_format == specs.ModelFormats.ONNX:
    #         onnx_model = ModelFileCRUD(self._user_id).read_onnx(model_id)
    #         predictions = onnx_model.run(None,
    #                             {'X': features.astype(np.float32).values})[0]
    #     elif model_info.save_format == specs.ModelFormats.PICKLE:
    #         model = ModelFileCRUD(self._user_id).read_pickle(model_id)
    #         predictions = model.predict(features)
    #     features[model_info.target] = predictions.tolist()
    #     return features.to_dict('list')
