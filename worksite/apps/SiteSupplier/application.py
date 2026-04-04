# This File is the Suppliers application controller. 
# It's purpose is to manage all Supplier related operations and routes. 
from fastapi import ( FastAPI, Request ) # pyright: ignore[reportMissingImports]
from fastapi.responses import FileResponse # pyright: ignore[reportMissingImports]

from config import (TEMPLATES)

from apps.SiteSupplier.routes import router 


app = FastAPI()
app.mount("/", router)
