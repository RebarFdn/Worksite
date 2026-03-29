# This File is the Projects application controller. 
# It's purpose is to manage all Project related operations and routes. 
from fastapi import ( FastAPI) # pyright: ignore[reportMissingImports]
from apps.SiteProject.routes import router as projectRouter


app = FastAPI()
app.mount("/", projectRouter)

