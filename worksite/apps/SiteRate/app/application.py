# This File is the Rates application controller. 
# It's purpose is to manage all Rate related operations and routes. 
from fastapi import ( FastAPI, Request ) # pyright: ignore[reportMissingImports]
from fastapi.responses import FileResponse # pyright: ignore[reportMissingImports]

from config import (TEMPLATES)
from core.utilities import ( check_paths, )

from config import STATIC_PATH


app = FastAPI()



@app.get("/rates")
async def rate_home(request:Request):
    return TEMPLATES.TemplateResponse( request=request, name="appTemplates/rate/index.html")

