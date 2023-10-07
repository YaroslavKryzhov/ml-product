from beanie import PydanticObjectId

from ml_api.apps.ml_models.repositories.repository_manager import ModelRepositoryManager
from ml_api.apps.ml_models.services.model_service import ModelService


class ModelForDataframeService:
    def __init__(self, user_id):
        self._user_id = user_id
        self.repository = ModelRepositoryManager(self._user_id)
        self.models_service = ModelService(self._user_id)

    async def _remove_from_model_predictions(self, model_id: PydanticObjectId,
                                             prediction_id: PydanticObjectId):
        return await self.repository.remove_prediction(model_id, prediction_id)

    # 4: DELETE OPERATIONS ----------------------------------------------------
    async def _delete_models_by_dataframe(self, dataframe_id: PydanticObjectId):
        dataframe_models = await self.repository.get_all_models_meta_by_dataframe(dataframe_id)
        for model in dataframe_models:
            await self.models_service.delete_model(model.id)
