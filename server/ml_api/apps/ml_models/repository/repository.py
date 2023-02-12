import os
import shutil
from typing import List, Dict
from datetime import datetime
import pickle

from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from ml_api.common.file_manager.base import FileCRUD


class ModelInfoCRUD:
    def __init__(self, session: Session, user):
        self.session = session
        self.user_id = str(user.id)

    # CREATE
    def create(
        self,
        model_name: str,
        csv_id: str,
        task_type: str,
        target: str,
        features: List,
        composition_type: str,
        composition_params: List,
        stage: str,
        report: Dict,
    ):
        """DEV USE: Save model info to PostgreDB"""
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

    # READ
    def read_by_name(self, model_name: str) -> CompositionFullInfo:
        filepath = self.file_path(model_name)
        model = (
            self.session.query(
                Model.id,
                Model.name,
                Model.csv_id,
                Model.features,
                Model.target,
                Model.create_date,
                Model.task_type,
                Model.composition_type,
                Model.composition_params,
                Model.stage,
                Model.report,
            )
            .filter(Model.filepath == filepath)
            .first()
        )
        if model:
            return CompositionFullInfo.from_orm(model)
        return None

    def read_all(self) -> List[CompositionShortInfo]:
        models = (
            self.session.query(
                Model.name,
                Model.csv_id,
                Model.features,
                Model.target,
                Model.create_date,
                Model.task_type,
                Model.composition_type,
                Model.stage,
            )
            .filter(Model.user_id == self.user_id)
            .all()
        )
        result = []
        for model in models:
            result.append(CompositionShortInfo.from_orm(model))
        return result

    # UPDATE
    def update(self, model_name: str, query: Dict):
        filepath = self.file_path(model_name)
        if query.get('name'):
            query['filepath'] = self.file_path(query['name'])
        self.session.query(Model).filter(Model.filepath == filepath).update(
            query
        )
        self.session.commit()

    # DELETE
    def delete(self, model_name: str):
        filepath = self.file_path(model_name)
        self.session.query(Model).filter(Model.filepath == filepath).delete()
        self.session.commit()


class ModelFileCRUD(FileCRUD):

    def read_onnx(self, model_uuid: str):
        model_path = self._get_path(model_uuid)
        # with open(model_path, 'rb') as handle:
        #     model = pickle.load(handle)

        # TODO: ONNX.read
        return model

    def download_onnx(self, model_uuid: str, filename: str):
        file_response = self.download(file_uuid=model_uuid, filename=filename)
        return file_response

    def save_onnx(self, model_uuid: str, model):
        """DEV USE: Save model in the pickle format"""
        model_path = self._get_path(model_uuid)
        # with open(model_path, 'wb') as handle:
        #     pickle.dump(model, handle, protocol=pickle.HIGHEST_PROTOCOL)

        # TODO: ONNX.write UUID.onnx
