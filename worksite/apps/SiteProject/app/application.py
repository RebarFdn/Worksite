# This File is the Projects application controller. 
# It's purpose is to manage all Project related operations and routes. 
from fastapi import ( FastAPI, Request ) # pyright: ignore[reportMissingImports]
from fastapi.responses import FileResponse # pyright: ignore[reportMissingImports]

from config import (TEMPLATES)
from core.utilities import ( check_paths, )

from config import STATIC_PATH


app = FastAPI()


#app.include_router( projectRouter )



@app.get("/")
async def index_home(request:Request):
    return TEMPLATES.TemplateResponse( request=request, name="index.html")


def test_static_path():
    assert STATIC_PATH.exists(), f"Static Path does not exist at {STATIC_PATH}"
    print(f"Static Path: {STATIC_PATH}")