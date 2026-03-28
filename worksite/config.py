from pathlib import Path
from starlette.config import Config # pyright: ignore[reportMissingImports]
from starlette.datastructures import Secret # pyright: ignore[reportMissingImports]
from fastapi.templating import Jinja2Templates # pyright: ignore[reportMissingImports]


# Documents Paths
BASE_PATH:Path = Path(__file__).parent
STATIC_PATH:Path = BASE_PATH / 'static'
TEMPLATES_PATH:Path = BASE_PATH / 'templates'

DOCS_PATH:Path = STATIC_PATH / 'docs'
IMAGES_PATH:Path = STATIC_PATH / 'imgs'
MAPS_PATH:Path = STATIC_PATH / 'maps'
PROFILES_PATH:Path = IMAGES_PATH / 'workers'
DATA_PATH:Path = BASE_PATH.parent / 'SiteLiteData'
# Logs
LOG_PATH:Path = Path.joinpath(BASE_PATH, 'logs')
SYSTEM_LOG_PATH:Path = Path.joinpath(LOG_PATH, 'system.log')
SERVER_LOG_PATH:Path = Path.joinpath(LOG_PATH, 'server.log')
APP_LOG_PATH:Path = Path.joinpath(LOG_PATH, 'app.log')


# File Paths
ENV_PATH:Path = Path.joinpath(BASE_PATH.parent, '.env') 
# Certificate and Key paths
CERT_PATH:Path = BASE_PATH.parent / '.keys'
# Icons Path
ICONS_PATH:Path = IMAGES_PATH / 'icons' 
FAVICON_PATH:Path = ICONS_PATH / 'favicon-16x16.png'
# Application Secrets
__config:Config = Config(ENV_PATH)

# Application Specific Settings

DEBUG:bool = True
DATABASE_URL:str = 'http://localhost:5984/'
SECRET_KEY:Secret = __config('SECRET_KEY',  cast=Secret)
DB_ADMIN:Secret  = __config('DB_ACCESS',  cast=Secret)
ADMIN_ACCESS:Secret  = __config('DB_SECRET',  cast=Secret)
DELAY:float = 0.0001
# Network
ALLOWED_HOSTS:list = ['127.0.0.1', 'localhost']
PORT:int = 9090
HOST:str = '0.0.0.0'

# Templates Engine
TEMPLATES = Jinja2Templates(TEMPLATES_PATH)

"""
system_user:User=User(
    name='SYSTEM',
    username='system',
    
)
"""

env = TEMPLATES.env

print(STATIC_PATH)