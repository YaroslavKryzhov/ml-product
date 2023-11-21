from typing import List

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from ml_api.apps.training_reports import specs, schemas
from ml_api.apps.users.routers import current_active_user
from ml_api.apps.users.model import User
from ml_api.apps.training_reports.repository import TrainingReportCRUD
from ml_api.apps.training_reports.model import Report


reports_router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
    responses={404: {"description": "Not found"}},
)


@reports_router.get("/", summary="Получить информацию об отчете об обучениии",
                    response_model=Report)
async def read_report(
    report_id: PydanticObjectId,
    user: User = Depends(current_active_user),
):
    """
        Возвращает информацию об отчете.

        - **report_id**: ID отчета
    """
    result = await TrainingReportCRUD(user.id).get(report_id)
    return result


@reports_router.get("/by_dataframe", summary="Получить информацию об отчетах, "
                                 "полученных при обучении на данном датафрейме",
                    response_model=List[Report])
async def read_reports_by_dataframe(
    dataframe_id: PydanticObjectId,
    user: User = Depends(current_active_user),
):
    """
        Возвращает список отчетов об обучении моделей,
        обученных на заданном датафрейме.

        - **dataframe_id**: ID датафрейма
    """
    result = await TrainingReportCRUD(user.id).get_by_dataframe_id(
        dataframe_id)
    return result


@reports_router.get("/by_model", summary="Получить информацию обо всех отчетах, "
                                 "полученных при обучении данной модели",
                    response_model=List[Report])
async def read_reports_by_model(
    model_id: PydanticObjectId,
    user: User = Depends(current_active_user),
):
    """
        Возвращает список отчетов об обучении модели, по её ID.

        - **model_id**: ID модели
    """
    result = await TrainingReportCRUD(user.id).get_by_model_id(
        model_id)
    return result


reports_specs_router = APIRouter(
    prefix="/reports/specs",
    tags=["Reports Specs"],
    responses={404: {"description": "Not found"}},
)


@reports_specs_router.get("/report_types")
def get_report_types():
    return {"report_types": [report_type.value for report_type in specs.ReportTypes]}


@reports_specs_router.get("/report_task_types")
def get_report_task_types():
    return {"report_task_types": [report_task_type.value for report_task_type
                                  in specs.ReportTypes]}


@reports_specs_router.get("/report_schemas/{report_task_type}")
def get_report_schema(report_task_type: specs.ReportTaskTypes):
    if report_task_type == specs.ReportTaskTypes.BINARY_CLASSIFICATION:
        return schemas.BinaryClassificationReport.schema()
    elif report_task_type == specs.ReportTaskTypes.MULTICLASS_CLASSIFICATION:
        return schemas.MulticlassClassificationReport.schema()
    elif report_task_type == specs.ReportTaskTypes.REGRESSION:
        return schemas.RegressionReport.schema()
    elif report_task_type == specs.ReportTaskTypes.CLUSTERING:
        return schemas.ClusteringReport.schema()
    elif report_task_type == specs.ReportTaskTypes.DIMENSIONALITY_REDUCTION:
        return schemas.DimensionalityReductionReport.schema()
    elif report_task_type == specs.ReportTaskTypes.OUTLIER_DETECTION:
        return schemas.OutlierDetectionReport.schema()
    else:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Unrecognized report type: '{report_task_type}'."
        )

