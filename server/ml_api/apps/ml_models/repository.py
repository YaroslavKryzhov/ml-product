from typing import List, Dict, Optional
from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from sqlalchemy import exc as sql_exceptions
from onnxruntime import InferenceSession

from fastapi import HTTPException, status
import pickle

from ml_api.common.file_manager.base import FileCRUD
from ml_api.apps.ml_models.models import Model
from ml_api.apps.ml_models.schemas import CompositionInfo, CompositionParams


class ModelInfoCRUD:
    def __init__(self, session: Session, user_id):
        self.session = session
        self.user_id = user_id

    # READ
    def get(self, model_id: UUID) -> CompositionInfo:
        model = (
            self.session.query(Model).filter(Model.id == model_id)
            .first()
        )
        if model is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Model with id {model_id} not found."
            )
        return CompositionInfo.from_orm(model)

    def get_all(self) -> List[CompositionInfo]:
        models = (
            self.session.query(Model).filter(Model.user_id == self.user_id)
            .all()
        )
        result = []
        for model in models:
            result.append(CompositionInfo.from_orm(model))
        return result

    # CREATE
    def create(
            self,
            filename: str,
            dataframe_id: UUID,
            features: List,
            target: str,
            task_type: str,
            composition_type: str,
            composition_params: List[CompositionParams],
            model_status: Optional[str],
            save_format: str,
            report: Optional[Dict] = None,
    ) -> CompositionInfo:
        new_obj = Model(
            filename=filename,
            user_id=self.user_id,
            dataframe_id=dataframe_id,
            features=features,
            target=target,
            created_at=str(datetime.now()),
            task_type=task_type,
            composition_type=composition_type,
            composition_params=composition_params,
            status=model_status,
            report=report,
            save_format=save_format
        )
        self.session.add(new_obj)
        try:
            self.session.commit()
        except sql_exceptions.IntegrityError as err:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(err)
            )
        except sql_exceptions.SQLAlchemyError as err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(err)
            )
        self.session.refresh(new_obj)
        return CompositionInfo.from_orm(new_obj)

    def update(self, model_id: UUID, query: Dict):
        try:
            res = self.session.query(Model).filter(Model.id == model_id
                ).update(query)
            if res == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Model with id {model_id} not found."
                )
        except sql_exceptions.IntegrityError as err:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(err)
            )
        except sql_exceptions.SQLAlchemyError as err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(err)
            )
        self.session.commit()

    # DELETE
    def delete(self, model_id: UUID):
        res = self.session.query(Model).filter(Model.id == model_id
                                                   ).delete()
        if res == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Model with id {model_id} not found."
            )
        self.session.commit()


class ModelFileCRUD(FileCRUD):

    def read_onnx(self, model_uuid: UUID):
        model_path = self._get_path(model_uuid)
        try:
            model = InferenceSession(f"{model_path}.onnx")
        except FileNotFoundError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Saved model with id {model_uuid} not found."
            )
        return model

    def download_model(self, model_uuid: UUID, filename: str) -> FileResponse:
        file_response = self.download(file_uuid=model_uuid, filename=filename)
        return file_response

    def save_onnx(self, model_uuid: UUID, model):
        """Save model in the ONNX format"""
        model_path = self._get_path(model_uuid)
        with open(f"{model_path}.onnx", "wb") as f:
            f.write(model.SerializeToString())

    """
    Some pickled models (like catboost) don't work properly after saving and load.
    """
    def read_pickle(self, model_uuid: UUID):
        model_path = self._get_path(model_uuid)
        try:
            with open(f"{model_path}.pickle", 'rb') as f:
                model = pickle.load(f)
        except FileNotFoundError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Saved model with id {model_uuid} not found."
            )
        return model

    def save_pickle(self, model_uuid: UUID, model):
        """Save model in the pickle format"""
        model_path = self._get_path(model_uuid)
        with open(f"{model_path}.pickle", "wb") as f:
            pickle.dump(model, f, protocol=pickle.HIGHEST_PROTOCOL)
