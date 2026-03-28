# This File is the main application controller. 
# It's purpose is to manage all application in the apps directory 
from fastapi import FastAPI # pyright: ignore[reportMissingImports]
from fastapi.staticfiles import StaticFiles # pyright: ignore[reportMissingImports]
from fastapi.middleware.cors import CORSMiddleware # pyright: ignore[reportMissingImports]

from config import (STATIC_PATH, TEMPLATES, TEMPLATES_PATH)
from .router import ( projectRouter )


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False,
    allow_origin_regex=None,
    expose_headers=[
        "Access-Control-Allow-Origin",
        "Access-Control-Allow-Cedentials",
        "Access-Control-Allow-Expose-Headers",
    ],
    max_age=3600,
)

# Serve Static Files
app.mount("/static", StaticFiles(directory=STATIC_PATH), name="static")
app.include_router( projectRouter )


if __name__ == '__main__':
    startup()