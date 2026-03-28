# This File is the main application controller. 
# It's purpose is to manage all application in the apps directory 
from fastapi import ( FastAPI, Request ) # pyright: ignore[reportMissingImports]
from fastapi.staticfiles import StaticFiles # pyright: ignore[reportMissingImports]
from fastapi.middleware.cors import CORSMiddleware # pyright: ignore[reportMissingImports]

from config import (STATIC_PATH, TEMPLATES, CERT_PATH, HOST, PORT, app_paths, settings)
from core.utilities import ( check_paths, )

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


if __name__ == '__main__':
    from uvicorn import run
    # startup the application
    startup()

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
   
    
    