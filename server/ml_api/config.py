from starlette.config import Config
from starlette.datastructures import Secret

config = Config('.env')

PROJECT_NAME = 'ML Project'
VERSION = '0.0.1'
API_PREFIX = "/api/v1"

MONGO_DATABASE_URI = config('MONGO_DATABASE_URI', cast=str, default='mongodb://zfCxePvYBPHa3w:jV9xRs8tZ@mongo_db:27017/think_mongo')
MONGO_DEFAULT_DB_NAME = config('MONGO_DEFAULT_DB_NAME', cast=str, default='think_mongo')


POSTGRES_USER = config('POSTGRES_USER', cast=str)
POSTGRES_PASSWORD = config('POSTGRES_PASSWORD', cast=Secret)
POSTGRES_SERVER = config('POSTGRES_SERVER', cast=str, default='db')
POSTGRES_PORT = config('POSTGRES_PORT', cast=str, default='5432')
POSTGRES_DB = config('POSTGRES_DB', cast=str)

DATABASE_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}'
DATABASE_ASYNC_URL = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}'

BROKER_URI = config('BROKER_URI', cast=str)
BACKEND_URI = config('BACKEND_URI', cast=str)

# JSON_LOGS = True if config("JSON_LOGS", default="0", cast=str) == "1" else False
# LOG_LEVEL = config("LOG_LEVEL", default="INFO", cast=str)
#
CENTRIFUGO_PUB_API = config("CENTRIFUGO_PUB_API", cast=str)
CENTRIFUDO_API_KEY = config("CENTRIFUDO_API_KEY", cast=str)
CENTRIFUGO_HMAC = config("CENTRIFUGO_HMAC", cast=str)

USER_SECRET = config("USER_SECRET", cast=str)

STAGE = config('STAGE', cast=str, default='DEVELOPMENT')

DOCS_URL = f'{API_PREFIX}/docs'
OPENAPI_URL = f'{API_PREFIX}/openapi.json'

ALLOW_ORIGINS = ['*']
HOST = config('HOST', cast=str, default='http://127.0.0.1')
if STAGE == 'PRODUCTION':
    ALLOW_ORIGINS = [HOST]

ROOT_DIR = '/data'
