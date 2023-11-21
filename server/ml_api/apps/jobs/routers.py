from typing import List

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends

from ml_api.apps.jobs import specs
from ml_api.apps.users.routers import current_active_user
from ml_api.apps.users.model import User
from ml_api.apps.jobs.services import BackgroundJobsService
from ml_api.apps.jobs.model import BackgroundJob

jobs_router = APIRouter(
    prefix="/background_jobs",
    tags=["Jobs"],
    responses={404: {"description": "Not found"}},
)


@jobs_router.get("/", summary="Получить информацию о job",
                 response_model=BackgroundJob)
async def get_job(
        job_id: PydanticObjectId,
        user: User = Depends(current_active_user),
):
    """
        Возвращает информацию о job.

        - **job_id**: ID отчета
    """
    return await BackgroundJobsService(user.id).get(job_id)


@jobs_router.get("/all",
                 summary="Получить информацию о всех jobs пользователя",
                 response_model=List[BackgroundJob])
async def get_all_jobs(
        user: User = Depends(current_active_user),
):
    """
        Возвращает список всех jobs.
    """
    return await BackgroundJobsService(user.id).get_all()


@jobs_router.get("/by_object", summary="Получить информацию обо всех jobs "
                                      "по объекту",
                 response_model=List[BackgroundJob])
async def get_jobs_by_object(
        object_type: specs.AvailableObjectTypes,
        object_id: PydanticObjectId,
        user: User = Depends(current_active_user),
):
    """
        Возвращает список job, связанных с объектом.

        - **object_type**: тип объекта: модель, датафрейм
        - **object_id**: ID объекта
    """
    return await BackgroundJobsService(user.id).get_by_object(
        object_type, object_id)


jobs_specs_router = APIRouter(
    prefix="/background_jobs/specs",
    tags=["Jobs Specs"],
    responses={404: {"description": "Not found"}},
)


@jobs_specs_router.get("/job_types")
def get_job_types():
    return {"job_types": [job_type.value for job_type
                          in specs.AvailableJobTypes]}


@jobs_specs_router.get("/object_types")
def get_object_types():
    return {"object_types": [object_type.value for object_type
                             in specs.AvailableObjectTypes]}


@jobs_specs_router.get("/job_statuses")
def get_job_types():
    return {"job_statuses": [job_status.value for job_status
                             in specs.JobStatuses]}
