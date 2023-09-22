import pandas as pd
from beanie import PydanticObjectId

from ml_api.apps.dataframes.services.dataframe_manager import DataframeManagerService
from ml_api.apps.dataframes.services.methods_manager import DataframeMethodsManagerService
from ml_api.apps.ml_models.services.metadata_manager import ModelMetadataManagerService
from ml_api.apps.ml_models.services.file_manager import ModelFileManagerService
from ml_api.apps.ml_models.models import ModelMetadata
from ml_api.apps.ml_models import errors, utils


class ModelPredictorService:
    def __init__(self, user_id, model_meta: ModelMetadata):
        self._user_id = user_id
        self.model_meta = model_meta
        self.dataframe_manager = DataframeManagerService(self._user_id)
        self.dataframe_methods_manager = DataframeMethodsManagerService(self._user_id)
        self.metadata_manager = ModelMetadataManagerService(self._user_id)
        self.file_manager = ModelFileManagerService(self._user_id)

    async def predict(self, dataframe_id: PydanticObjectId, apply_pipeline=True):
        if apply_pipeline:
            train_df_id = self.model_meta.dataframe_id
            await self.dataframe_methods_manager.copy_pipeline(train_df_id, dataframe_id)

        features, _ = await self.dataframe_manager.get_feature_target_df(
            dataframe_id)
        if sorted(features.columns.tolist()) != sorted(self.model_meta.feature_columns):
            raise errors.FeaturesNotEqualError()
        model = await self.file_manager.load_model_from_file(self.model_meta.id)
        predictions = pd.Series(model.predict(features))
        results_df = utils.get_predictions_df(features, predictions)
        return results_df
