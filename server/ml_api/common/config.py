from databases import DatabaseURL
from starlette.config import Config
from starlette.datastructures import Secret

config = Config('.env')

# config = Config('/opt/project/server/.env')

S2_CLIENT_ID = config('S2_CLIENT_ID', cast=str)
S2_CLIENT_SECRET = config('S2_CLIENT_SECRET', cast=str)
S2_PRODUCT_ID = config('S2_PRODUCT_ID', cast=str)

PROJECT_NAME = 'Rebels AI services (RAIS)'
VERSION = '1.0.0'
API_VERSION = config('API_VERSION', cast=str, default='v1')
API_PREFIX = f'/api/{API_VERSION}'

SECRET_KEY = config('SECRET_KEY', cast=Secret, default='CHANGEME')

POSTGRES_USER = config('POSTGRES_USER', cast=str)
POSTGRES_PASSWORD = config('POSTGRES_PASSWORD', cast=Secret)
POSTGRES_SERVER = config('POSTGRES_SERVER', cast=str, default='db')
POSTGRES_PORT = config('POSTGRES_PORT', cast=str, default='5432')
POSTGRES_DB = config('POSTGRES_DB', cast=str)

DATABASE_URL = config(
  'DATABASE_URL',
  cast=DatabaseURL,
  default=f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}'
)

STAGE = config('STAGE', cast=str, default='DEVELOPMENT')
DOCS_URL = f'{API_PREFIX}/docs'
OPENAPI_URL = f'{API_PREFIX}/openapi.json'

ALLOW_ORIGINS = ['*']
HOST_TWITTER = config('HOST_TWITTER', cast=str)
HOST = config('HOST', cast=str, default='http://127.0.0.1')
if STAGE == 'PRODUCTION':
    ALLOW_ORIGINS = [HOST]

GOOGLE_CLIENT_ID = config('GOOGLE_CLIENT_ID', cast=str)
GOOGLE_CLIENT_SECRET = config('GOOGLE_CLIENT_SECRET', cast=str)
GOOGLE_CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
API_ALGORITHM = 'HS256'
API_ACCESS_TOKEN_EXPIRE_MINUTES = config('API_ACCESS_TOKEN_EXPIRE_MINUTES', cast=float, default=15)
AUTH_TOKEN_GOOGLE_URL = f'{API_PREFIX}/auth/token'
AUTH_TOKEN__PASSWD_URL = f'{API_PREFIX}/auth/tokenPasswd'
TWITTER_API_KEY = config('TWITTER_API_KEY', cast=str)
TWITTER_API_SECRET = config('TWITTER_API_SECRET', cast=str)

FIRST_SUPERUSER = config('FIRST_SUPERUSER', cast=str)
FIRST_SUPERUSER_EMAIL = config('FIRST_SUPERUSER_EMAIL', cast=str)
FIRST_SUPERUSER_PASSWORD = config('FIRST_SUPERUSER_PASSWORD', cast=str)

WORKSPACES_DIR = config('WORKSPACES_DIR', cast=str)
TOOLS_DIR = config('TOOLS_DIR', cast=str)

ROOT_DIR_SIDE_CODE = ''
ROOT_DIR_CUSTOM_MODULES = ''

JSON_LOGS = True if config("JSON_LOGS", default="0", cast=str) == "1" else False
LOG_LEVEL = config("LOG_LEVEL", default="INFO", cast=str)

CENTRIFUGO_PUB_API = config("CENTRIFUGO_PUB_API", default="https://services.rebels.ai/centrifugo", cast=str)
CENTRIFUDO_API_KEY = config("CENTRIFUDO_API_KEY", cast=str)
CENTRIFUGO_HMAC = config("CENTRIFUGO_HMAC", cast=str)

CHAT_BOT_URL = config("CHAT_BOT_URL",  cast=str)

MONGO_CONNECTION_STRING = config("MONGO_CONNECTION_STRING", cast=str)

AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID",  cast=str)
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY",  cast=str)
BUCKET = config("BUCKET",  cast=str)
USER_POOL_ID = config("USER_POOL_ID",  cast=str)
CLIENT_ID = config("CLIENT_ID",  cast=str)
ACCOUNT_ID = config("ACCOUNT_ID",  cast=str)
IDENTITY_POOL_ID = config("IDENTITY_POOL_ID",  cast=str)
PROVIDER = config("PROVIDER",  cast=str)
PUBLIC_FOLDER = config("PUBLIC_FOLDER",  cast=str)
POLICY_PREFIX = config("POLICY_PREFIX",  cast=str)
ROLE_PREFIX = config("ROLE_PREFIX",  cast=str)
GROUP_PREFIX = config("GROUP_PREFIX",  cast=str)
BUCKET_RESOURCE = f"arn:aws:s3:::{BUCKET}"


"""


"""


from ml_api.common.postgre_config import (
    DATABASE_USER,
    DATABASE_PASSWORD,
    DATABASE_PORT,
    DATABASE_HOST,
)

PROJECT_NAME = 'ML Project'
VERSION = '0.0.1'

DEFAULT_DB_NAME = 'ml_project'
DATABASE_URL = f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DEFAULT_DB_NAME}'

DATABASE_ASYNC_URL = f'postgresql+asyncpg://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DEFAULT_DB_NAME}'

ALLOW_ORIGINS = ['*']

ROOT_DIR = '/data'
