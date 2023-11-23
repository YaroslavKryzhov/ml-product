from typing import List

from bunnet import PydanticObjectId

from ml_api.apps.dataframes import specs, schemas
from ml_api.apps.dataframes.model import DataFrameMetadata
from ml_api.apps.dataframes.repositories.repository_manager import \
    DataframeRepositoryManager
from ml_api.apps.dataframes.services.processors.methods_applier import \
    MethodsApplierValidator
from ml_api.apps.dataframes.services.processors.feature_selector import \
    FeatureSelectorValidator
from ml_api.apps.dataframes.services.dataframe_service import \
    DataframeService
from ml_api.apps.dataframes.services.methods_service import \
    DataframeMethodsService
from ml_api.apps.dataframes.services.jobs_manager import DataframeJobsManager
from ml_api import config


class DataframeMethodsAsyncService:
    """
    Применяет функции к датафрейму и сохраняет результаты в базу.
    """

    def __init__(self, user_id):
        self._user_id = user_id
        self.repository = DataframeRepositoryManager(self._user_id)
        self.dataframe_service = DataframeService(self._user_id)
        self.methods_service = DataframeMethodsService(self._user_id)

    def run_feature_importances(
            self,
            dataframe_id: PydanticObjectId,
            task_type: specs.FeatureSelectionTaskType,
            feature_selection_params: List[schemas.SelectorMethodParams]
    ) -> schemas.FeatureSelectionSummary:
        self.dataframe_service._ensure_not_prediction(dataframe_id)
        self.dataframe_service._check_for_target_feature(dataframe_id)
        validated_params = FeatureSelectorValidator().validate_params(
            feature_selection_params)
        if config.USE_CELERY:
            return DataframeJobsManager(self._user_id).process_feature_importances_async(
                dataframe_id, task_type, validated_params)
        else:
            return self.methods_service._process_feature_importances(
                dataframe_id, task_type, validated_params)

    def apply_changing_methods(
            self, dataframe_id: PydanticObjectId,
            methods_params: List[schemas.ApplyMethodParams],
            new_filename: str = None) -> DataFrameMetadata:
        self.dataframe_service._ensure_not_prediction(dataframe_id)
        self.dataframe_service._check_filename_exists(new_filename)
        validated_params = MethodsApplierValidator().validate_params(
            methods_params)
        if config.USE_CELERY:
            return DataframeJobsManager(self._user_id).process_changing_methods_async(
                dataframe_id, validated_params, new_filename)
        else:
            return self.methods_service._process_changing_methods(
                dataframe_id, validated_params, new_filename)

    def copy_pipeline(self, id_from: PydanticObjectId,
                      id_to: PydanticObjectId,
                      new_filename: str) -> DataFrameMetadata:
        self.dataframe_service._check_filename_exists(new_filename)
        self.dataframe_service._ensure_not_prediction(id_from)
        self.dataframe_service._ensure_not_prediction(id_to)
        pipeline_from_source_df = self.repository.get_pipeline(id_from)
        validated_params = MethodsApplierValidator().validate_params(
            pipeline_from_source_df)
        if config.USE_CELERY:
            return DataframeJobsManager(self._user_id).process_changing_methods_async(
                id_to, validated_params, new_filename)
        else:
            return self.methods_service._process_changing_methods(
                id_to, validated_params, new_filename)

