from starlette.config import Config

config = Config('.env')

PROJECT_NAME = 'ML Project'
VERSION = '0.0.1'
API_PREFIX = "/api/v1"
DOCS_URL = f'{API_PREFIX}/docs'
OPENAPI_URL = f'{API_PREFIX}/openapi.json'
ALLOW_ORIGINS = ['*']

STAGE = config('STAGE', cast=str, default='DEVELOPMENT')
if STAGE == 'PRODUCTION':
    HOST = config('HOST', cast=str, default='http://127.0.0.1')
    ALLOW_ORIGINS = [HOST]
    DOCS_URL = None
    OPENAPI_URL = None

MONGO_USER = config('MONGO_USER', cast=str)
MONGO_PASSWORD = config('MONGO_PASSWORD', cast=str)
MONGO_DB_NAME = config('MONGO_INITDB_db', cast=str, default="ml_product_mongo")
MONGO_DATABASE_URI = f'mongodb://{MONGO_USER}:{MONGO_PASSWORD}@mongo_db:27017/{MONGO_DB_NAME}?authSource={MONGO_DB_NAME}'

CENTRIFUGO_PUB_API = "http://centrifugo:8000/api"
CENTRIFUDO_API_KEY = config("CENTRIFUDO_API_KEY", cast=str)
CENTRIFUGO_HMAC = config("CENTRIFUGO_HMAC", cast=str)

RABBITMQ_DEFAULT_USER = config('RABBITMQ_DEFAULT_USER', cast=str)
RABBITMQ_DEFAULT_PASS = config('RABBITMQ_DEFAULT_PASS', cast=str)

# Celery
BROKER_URI = f"amqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@rabbitmq:5672"
BACKEND_URI = MONGO_DATABASE_URI

USER_SECRET = config("USER_SECRET", cast=str)

ROOT_DIR = '/data'
USE_CELERY = True
USE_HYPEROPT = False
