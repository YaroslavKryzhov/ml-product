import sys
import logging
# from loguru import logger
#
#
# from ml_api.common.config import LOG_LEVEL, JSON_LOGS
#
#
# class InterceptHandler(logging.Handler):
#     def emit(self, record):
#         # Get corresponding Loguru level if it exists
#         try:
#             level = logger.level(record.levelname).name
#         except ValueError:
#             level = record.levelno
#
#         # Find caller from where originated the logged message
#         frame, depth = logging.currentframe(), 2
#         while frame.f_code.co_filename == logging.__file__:
#             frame = frame.f_back
#             depth += 1
#         logger.opt(depth=depth,  exception=record.exc_info, colors=True).log(level, record.getMessage())
#
#
# def setup_logging():
#     # Setup logging
#     log_level = logging.getLevelName(LOG_LEVEL)
#     # intercept everything at the root logger
#     logging.root.handlers = [InterceptHandler()]
#     logging.root.setLevel(log_level)
#     # remove every other logger's handlers
#     # and propagate to root logger
#     for name in logging.root.manager.loggerDict.keys():
#         logging.getLogger(name).handlers = []
#         logging.getLogger(name).propagate = True
#     # configure loguru
#     logger.configure(handlers=[{"sink": sys.stdout, "serialize": JSON_LOGS}])
#     logger.add("/quimly_data/logs/quimly.log", rotation="100 MB")