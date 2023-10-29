from typing import List, Dict, Optional

from beanie import PydanticObjectId
from pymongo.errors import DuplicateKeyError

from ml_api.apps.ml_models import schemas, specs, errors
from ml_api.apps.ml_models.model import ModelMetadata


class ModelMetaCRUD:
    def __init__(self, user_id: PydanticObjectId):
        self.user_id = user_id

    async def get(self, model_id: PydanticObjectId) -> ModelMetadata:
        model_meta = await ModelMetadata.get(model_id)
        if model_meta is None:
            raise errors.ModelNotFoundError(model_id)
        return model_meta

    async def get_all(self) -> List[ModelMetadata]:
        model_metas = await ModelMetadata.find(
            ModelMetadata.user_id == self.user_id).to_list()
        return model_metas

    async def get_by_dataframe_id(self, dataframe_id: PydanticObjectId
                                  ) -> List[ModelMetadata]:
        models = await ModelMetadata.find(
            ModelMetadata.user_id == self.user_id).find(
            ModelMetadata.dataframe_id == dataframe_id).to_list()
        return models

    async def create(self,
                     filename: str,
                     dataframe_id: PydanticObjectId,
                     is_composition: bool,
                     task_type: specs.AvailableTaskTypes,
                     model_params: schemas.ModelParams,
                     params_type: specs.AvailableParamsTypes,
                     feature_columns: List[str],
                     target_column: str,
                     test_size: float,
                     stratify: bool,
                     composition_model_ids: Optional[List[PydanticObjectId]] = None
                     ) -> ModelMetadata:
        new_obj = ModelMetadata(
            filename=filename,
            user_id=self.user_id,
            dataframe_id=dataframe_id,
            is_composition=is_composition,
            task_type=task_type,
            model_params=model_params,
            params_type=params_type,
            feature_columns=feature_columns,
            target_column=target_column,
            test_size=test_size,
            stratify=stratify,
            composition_model_ids=composition_model_ids
        )
        try:
            await new_obj.insert()
        except DuplicateKeyError:
            raise errors.FilenameExistsUserError(filename)
        return new_obj

    async def update(self, model_id: PydanticObjectId, query: Dict
                     ) -> ModelMetadata:
        model_meta = await ModelMetadata.get(model_id)
        if model_meta is None:
            raise errors.ModelNotFoundError(model_id)
        await model_meta.update(query)
        model_meta_updated = await ModelMetadata.get(model_id)
        return model_meta_updated

    async def delete(self, model_id: PydanticObjectId) -> ModelMetadata:
        model_meta = await ModelMetadata.get(model_id)
        if model_meta is None:
            raise errors.ModelNotFoundError(model_id)
        await model_meta.delete()
        return model_meta
