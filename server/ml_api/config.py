from starlette.config import Config

config = Config('.env')

PROJECT_NAME = 'ML Project'
VERSION = '0.0.1'
API_PREFIX = "/api/v1"
RUN_ASYNC_TASKS = config('RUN_ASYNC_TASKS', cast=bool, default=True)

MONGO_DATABASE_URI = config('MONGO_DATABASE_URI', cast=str, default='mongodb://zfCxePvYBPHa3w:jV9xRs8tZ@mongo_db:27017/think_mongo')
MONGO_DEFAULT_DB_NAME = config('MONGO_DEFAULT_DB_NAME', cast=str, default='think_mongo')

# BROKER_URI = config('BROKER_URI', cast=str, default="redis://redis:6379/0")
# BACKEND_URI = config('BACKEND_URI', cast=str, default="redis://redis:6379/0")

# JSON_LOGS = True if config("JSON_LOGS", default="0", cast=str) == "1" else False
# LOG_LEVEL = config("LOG_LEVEL", default="INFO", cast=str)
#
CENTRIFUGO_PUB_API = config("CENTRIFUGO_PUB_API", cast=str, default="http://centrifugo:8000/api")
CENTRIFUDO_API_KEY = config("CENTRIFUDO_API_KEY", cast=str, default="9o_XDiSJpYPi11k4P90hoWTWZz2_nTNAkxB4gRgnZbg")
CENTRIFUGO_HMAC = config("CENTRIFUGO_HMAC", cast=str, default="46b38493-147e-4e3f-86e0-dc5ec54f5133")

USER_SECRET = config("USER_SECRET", cast=str, default="dfgb34g37obdjkfgb983bkjfdg")

STAGE = config('STAGE', cast=str, default='DEVELOPMENT')

DOCS_URL = f'{API_PREFIX}/docs'
OPENAPI_URL = f'{API_PREFIX}/openapi.json'

ALLOW_ORIGINS = ['*']
HOST = config('HOST', cast=str, default='http://127.0.0.1')
if STAGE == 'PRODUCTION':
    ALLOW_ORIGINS = [HOST]

ROOT_DIR = '/data'
