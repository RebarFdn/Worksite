from pathlib import Path
from starlette.config import Config # pyright: ignore[reportMissingImports]
from starlette.datastructures import Secret # pyright: ignore[reportMissingImports]
from fastapi.templating import Jinja2Templates # pyright: ignore[reportMissingImports]
from pydantic_settings import BaseSettings # pyright: ignore[reportMissingImports]

# Directory Paths
BASE_PATH:Path = Path(__file__).parent
CORE_PATH:Path = BASE_PATH / 'core'
STATIC_PATH:Path = CORE_PATH / 'static'
TEMPLATES_PATH:Path = CORE_PATH / 'baseTemplates'

DOCS_PATH:Path = CORE_PATH / 'docs'
SCRIPTS_PATH:Path = STATIC_PATH / 'js'
STYLES_PATH:Path = STATIC_PATH / 'css'
IMAGES_PATH:Path = STATIC_PATH / 'imgs'
MAPS_PATH:Path = STATIC_PATH / 'maps'
ICONS_PATH:Path = IMAGES_PATH / 'icons' 
PROFILES_PATH:Path = IMAGES_PATH / 'workers'
DATA_PATH:Path = BASE_PATH.parent.parent / 'SiteLiteData'
LOG_PATH:Path = Path.joinpath(BASE_PATH.parent, 'logs')
# Certificate and Key paths
CERT_PATH:Path = BASE_PATH.parent / '.keys'

# File paths
SYSTEM_LOG_FILE:Path = Path.joinpath(LOG_PATH, 'system.log')
SERVER_LOG_FILE:Path = Path.joinpath(LOG_PATH, 'server.log')
APP_LOG_FILE:Path = Path.joinpath(LOG_PATH, 'app.log')
ENV_FILE:Path = Path.joinpath(BASE_PATH.parent, '.env') 
FAVICON_FILE:Path = ICONS_PATH / 'favicon-16x16.png'


# Application Secrets
__config:Config = Config(ENV_FILE)

# Application Specific Settings
DEBUG:bool = True
DATABASE_URL:str = 'http://localhost:5984/'
SECRET_KEY:Secret = __config('SECRET_KEY',  cast=Secret)
DB_ADMIN:Secret  = __config('DB_ACCESS',  cast=Secret)
ADMIN_ACCESS:Secret  = __config('DB_SECRET',  cast=Secret)

# Network
ALLOWED_HOSTS:list = ['127.0.0.1', 'localhost']
PORT:int = 9095
HOST:str = '0.0.0.0'

THROTTLE:float = 0.01

# Templates Engine
TEMPLATES = Jinja2Templates(TEMPLATES_PATH)

template_env = TEMPLATES.env

app_paths = [BASE_PATH, CORE_PATH, STATIC_PATH, TEMPLATES_PATH, DOCS_PATH,  SCRIPTS_PATH, STYLES_PATH, IMAGES_PATH, MAPS_PATH, ICONS_PATH, PROFILES_PATH, DATA_PATH, LOG_PATH]

"""
system_user:User=User(
    name='SYSTEM',
    username='system',
    
)
"""
class Settings(BaseSettings):
    app_name: str = "Worksite"
    admin_email: str = "admin@worksite.com"
    items_per_user: int = 50

settings = Settings()