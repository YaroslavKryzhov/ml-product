from typing import Optional, List
from uuid import UUID

from fastapi.responses import JSONResponse
from fastapi import status, HTTPException
import numpy as np
from skl2onnx import to_onnx

from ml_api.apps.ml_models.repository import ModelInfoCRUD, ModelFileCRUD
from ml_api.apps.ml_models import schemas, specs
from ml_api.apps.dataframes.services.services import DataframeManagerService
from ml_api.apps.ml_models.services.params_searcher import AutoParamsSearch
from ml_api.apps.ml_models.services.composition_construstor import \
    CompositionConstructor
from ml_api.apps.ml_models.services.composition_trainer import \
    CompositionTrainer


class ModelManagerService:
    def __init__(self, db, user_id):
        self._db = db
        self._user_id = user_id

    # 1: FILE MANAGEMENT OPERATIONS -------------------------------------------
    def download_model(self, model_id: UUID):
        model_info = ModelInfoCRUD(self._db, self._user_id).get(model_id)
        response = ModelFileCRUD(self._user_id).download_model(
            model_uuid=model_id, filename=model_info.filename)
        return response

    def rename_model(self, model_id: UUID, new_filename: str):
        model_info = ModelInfoCRUD(self._db, self._user_id).get(model_id)
        query = {'filename': f"{new_filename}.{model_info.save_format.value}"}
        ModelInfoCRUD(self._db, self._user_id).update(model_id, query)

    def delete_model(self, model_id: str):
        ModelInfoCRUD(self._db, self._user_id).delete(model_id)
        ModelFileCRUD(self._user_id).delete(model_id)

    # 2: GET OPERATIONS -------------------------------------------------------
    def get_model_info(self, model_id: str) -> schemas.CompositionInfo:
        return ModelInfoCRUD(self._db, self._user_id).get(model_id)

    def get_all_models_info(self) -> List[schemas.CompositionInfo]:
        return ModelInfoCRUD(self._db, self._user_id).get_all()

    def create_model(
            self,
            task_type: specs.AvailableTaskTypes,
            composition_type: specs.AvailableCompositionTypes,
            composition_params: List[schemas.CompositionParams],
            dataframe_id: UUID,
            model_name: str,
            save_format: specs.ModelSaveFormats
    ) -> schemas.CompositionInfo:
        if (composition_type == specs.AvailableCompositionTypes.NONE and
                len(composition_params) != 1):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="If composition type is 'NONE' there should be one model",
            )

        feature_columns, target_column = DataframeManagerService(
            self._db, self._user_id).get_feature_target_column_names(
            dataframe_id=dataframe_id)

        model_info = ModelInfoCRUD(self._db, self._user_id).create(
            filename=f"{model_name}.{save_format.value}",
            dataframe_id=dataframe_id,
            features=feature_columns,
            target=target_column,
            task_type=task_type.value,
            composition_type=composition_type.value,
            composition_params=composition_params,
            model_status=specs.CompositionStatuses.BUILD.value,
            save_format=save_format.value
        )
        return model_info

    def prepare_model(self, model_info: schemas.CompositionInfo,
                      params_type: specs.AvailableParamsTypes):
        dataframe_id = model_info.dataframe_id
        composition_params = model_info.composition_params

        features, target = DataframeManagerService(self._db, self._user_id
            ).get_feature_target_df(dataframe_id=dataframe_id)

        if (model_info.task_type == specs.AvailableTaskTypes.CLASSIFICATION
                and target.nunique() == 1):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Only one class label in dataframe with id {dataframe_id}",
            )

        if params_type == specs.AvailableParamsTypes.AUTO:
            composition_params = AutoParamsSearch(
                task_type=model_info.task_type,
                composition_params=model_info.composition_params,
                features=features,
                target=target,
            ).search_params()
            query = {'composition_params': composition_params}
            ModelInfoCRUD(self._db, self._user_id).update(
                model_id=model_info.id, query=query)

        composition = CompositionConstructor(
            task_type=model_info.task_type,
            composition_type=model_info.composition_type,
            composition_params=composition_params,
        ).build_composition()
        return composition

    def train_model(self, model_info: schemas.CompositionInfo, composition,
                    test_size: Optional[float] = 0.2):
        dataframe_id = model_info.dataframe_id

        features, target = DataframeManagerService(self._db, self._user_id
            ).get_feature_target_df(dataframe_id=dataframe_id)

        query = {'status': specs.CompositionStatuses.TRAINING.value}
        ModelInfoCRUD(self._db, self._user_id).update(
            model_id=model_info.id, query=query)
        try:
            model, metrics = CompositionTrainer(
                task_type=model_info.task_type,
                composition=composition,
                model_id=model_info.id,
                features=features,
                target=target,
                test_size=test_size,
            ).validate_model()
        except Exception as e:
            query = {'status': specs.CompositionStatuses.PROBLEM.value}
            ModelInfoCRUD(self._db, self._user_id).update(
                model_id=model_info.id, query=query)
            raise e

        query = {'report': metrics, 'status': specs.CompositionStatuses.TRAINED.value}
        ModelInfoCRUD(self._db, self._user_id).update(
            model_id=model_info.id, query=query)
        self._save_model(
            model_id=model_info.id,
            model=model,
            feature_example=features[:1].astype(np.float32).values,
            save_format=model_info.save_format
        )

    def _save_model(self, model_id: UUID, model,
                    feature_example: Optional[np.ndarray],
                    save_format: specs.ModelSaveFormats):
        try:
            if save_format == specs.ModelSaveFormats.ONNX:
                onx = to_onnx(model, feature_example)
                ModelFileCRUD(self._user_id).save_onnx(model_uuid=model_id, model=onx)
            elif save_format == specs.ModelSaveFormats.PICKLE:
                ModelFileCRUD(self._user_id).save_pickle(model_uuid=model_id, model=model)
        except Exception as e:
            query = {'status': specs.CompositionStatuses.PROBLEM.value}
            ModelInfoCRUD(self._db, self._user_id).update(
                model_id=model_id, query=query)
            raise e

    def predict_on_model(self, dataframe_id: UUID, model_id: UUID):
        features = DataframeManagerService(self._db, self._user_id
            ).get_feature_df(dataframe_id=dataframe_id)
        model_info = ModelInfoCRUD(self._db, self._user_id).get(model_id)
        if features.columns.to_list() != model_info.features:
            return JSONResponse(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                content="Features in doc and in model training history are "
                        "different",
            )
        if model_info.save_format == specs.ModelSaveFormats.ONNX:
            onnx_model = ModelFileCRUD(self._user_id).read_onnx(model_id)
            predictions = onnx_model.run(None,
                                {'X': features.astype(np.float32).values})[0]
        elif model_info.save_format == specs.ModelSaveFormats.PICKLE:
            model = ModelFileCRUD(self._user_id).read_pickle(model_id)
            predictions = model.predict(features)
        features[model_info.target] = predictions.tolist()
        return features.to_dict('list')
