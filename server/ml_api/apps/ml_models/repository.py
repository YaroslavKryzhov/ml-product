from typing import List, Dict
from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from sqlalchemy import exc as sql_exceptions
from onnxruntime import InferenceSession
from google.protobuf.message import Message
from fastapi import HTTPException, status

from ml_api.common.file_manager.base import FileCRUD
from ml_api.apps.ml_models.models import Model


class ModelInfoCRUD:
    def __init__(self, session: Session, user):
        self.session = session
        self.user_id = str(user.id)

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
        #     TODO: rewrite
        self,
        model_name: str,
        csv_id: UUID,
        task_type: str,
        target: str,
        features: List,
        composition_type: str,
        composition_params: List,
        stage: str,
        report: Dict,
    ):
        new_obj = Model(
            name=model_name,
            filepath=self.file_path(model_name),
            user_id=self.user_id,
            csv_id=csv_id,
            features=features,
            target=target,
            create_date=str(datetime.now()),
            task_type=task_type,
            composition_type=composition_type,
            composition_params=composition_params,
            stage=stage,
            report=report,
        )
        self.session.add(new_obj)
        self.session.commit()

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
                detail=f"Model with id {model_uuid} not found."
            )
        return model

    def download_onnx(self, model_uuid: UUID, filename: str) -> FileResponse:
        file_response = self.download(file_uuid=model_uuid, filename=filename)
        return file_response

    def save_onnx(self, model_uuid: UUID, model: Message):
        """Save model in the ONNX format"""
        model_path = self._get_path(model_uuid)
        with open(f"{model_path}.onnx", "wb") as f:
            f.write(model.SerializeToString())

    """
    DEPRECATED: if you want to return PICKLE format,
    you need to write new predict methods, because of different ONNX logic:
    https://onnx.ai/sklearn-onnx/introduction.html#
    """
    # def read_pickle(self, model_uuid: UUID):
    #     model_path = self._get_path(model_uuid)
    #     with open(f"{model_path}.pickle", 'rb') as f:
    #         model = pickle.load(f)
    #     return model

    # def save_pickle(self, model_uuid: UUID, model):
    #     """Save model in the pickle format"""
    #     model_path = self._get_path(model_uuid)
    #     with open(f"{model_path}.pickle", "wb") as f:
    #         pickle.dump(model, f, protocol=pickle.HIGHEST_PROTOCOL)
