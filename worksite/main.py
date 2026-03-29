# This File is the main application controller. 
# It's purpose is to manage all application in the apps directory 
from fastapi import ( FastAPI, Request ) # pyright: ignore[reportMissingImports]
from fastapi.responses import FileResponse # pyright: ignore[reportMissingImports]
from fastapi.staticfiles import StaticFiles # pyright: ignore[reportMissingImports]
from fastapi.middleware.cors import CORSMiddleware # pyright: ignore[reportMissingImports]

from config import (STATIC_PATH, TEMPLATES, FAVICON_FILE, CERT_PATH, HOST, PORT, app_paths, settings)
from core.utilities import ( check_paths, )
# Importing Applications
from apps.SiteUser.app.application import app as user_app
from apps.SiteProject.app.application import app as project_app
from apps.SiteRate.app.application import app as rate_app
from apps.SiteSupplier.app.application import app as supplier_app
from apps.SiteWorker.app.application import app as worker_app


def startup():
    check_paths(paths=app_paths)


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
#app.include_router( projectRouter )
app.mount("/user", user_app)
app.mount("/project", project_app)
app.mount("/rate", rate_app)
app.mount("/supplier", supplier_app)
app.mount("/worker", worker_app)



@app.get("/")
async def index_home(request:Request):
    return TEMPLATES.TemplateResponse( request=request, name="index.html")


@app.get("/info")
async def info():
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user,
    }


@app.get("/favicon.ico")
async def favicon(): 
    """ Serves The Site Favicon file."""   
    return FileResponse(FAVICON_FILE)


if __name__ == '__main__':
    from uvicorn import run # pyright: ignore[reportMissingImports]
    # startup the application
    #startup()
   

    key_path = CERT_PATH / 'site.key'
    cert_path = CERT_PATH / 'site.crt' 

    if not key_path.exists() or not cert_path.exists():
        print(f"Certificate or key file not found.")
        print('...')
        print(f'Server is running in an insecure mode at HOST {HOST}. on PORT {PORT}..!')
        print('...')
        # Start the server in unsecure mode 
        try:
            run(
                app=app, 
                host=HOST, 
                port=PORT, 
                ssl_certfile=None, 
                ssl_keyfile=None 
            )
        except Exception as e:
            print(str(e))
    else:

        print(f"Certificate and key file found...")        
        print(f'Server is running Securely at HOST {HOST}. on PORT {PORT}..!')
        print('Press Ctrl+C to stop the server.')        
        # Start the server with SSL
        try:
            run(
                app=app, 
                host=HOST, 
                port=PORT, 
                ssl_certfile=cert_path, 
                ssl_keyfile=key_path 
            )
        except Exception as e:
            print(str(e))
   
    
    