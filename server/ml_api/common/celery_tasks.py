# from celery import Task
# from beanie import init_beanie
#
# from beanie import PydanticObjectId
# from fastapi import HTTPException
#
# from ml_api.apps.dataframes import specs, schemas
# from ml_api.apps.dataframes.services.methods_service import \
#     DataframeMethodsService
# from ml_api.common.jobs_manager.base import JobsManager
#
#
#
# class BackgroundTask(Task):
#     abstract = True
#
#     def _process_http_exception(self, err: HTTPException,
#                                       job: BackgroundJob):
#         # print(traceback.format_exc())
#         error_type = type(err).__name__
#         error_description = str(err.detail)
#         message = f"{error_type}: {error_description}"
#         job_info = await self.job_service.error(job.id, message)
#         return job_info
#
#     def _process_exception(self, err: Exception, job: BackgroundJob):
#         # print(traceback.format_exc())
#         error_type = type(err).__name__
#         error_description = str(err)
#         message = f"{error_type}: {error_description}"
#         job_info = await self.job_service.error(job.id, message)
#         return job_info
#
#     def after_return(self, status, retval, task_id, args, kwargs, einfo):
#         self._publish_job(job_info)
#
#
# @app_celery.task(base=BackgroundTask, name="apply_function", bind=True)
# def apply_function_celery(self, user_id: str, dataframe_id: str, function_name: str, params):
#     self.user_id = user_id
#     try:
#         with Session() as db:
#             function_name = dataframe_specs.AvailableFunctions(function_name)
#             DataframeManagerService(db, user_id).apply_function(dataframe_id, function_name, params)
#     except ConnectionError as e:
#         logger.error(e)
#         raise Exception("Can't connect to database")
#     return True
#
#
