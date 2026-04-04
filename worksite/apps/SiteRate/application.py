# This File is the Rates application controller. 
# It's purpose is to manage all Rate related operations and routes. 
from fastapi import ( FastAPI, Request ) # pyright: ignore[reportMissingImports]
from fastapi.responses import FileResponse # pyright: ignore[reportMissingImports]
from config import (TEMPLATES)
from core.utilities import ( check_paths, )
from config import STATIC_PATH

from apps.SiteRate.routes import router 


app = FastAPI()
app.mount("/", router)
