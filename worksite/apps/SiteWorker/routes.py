# SiteWorker Routes
from typing import Any
from pathlib import Path
from PIL import Image
from functools import lru_cache
from fastapi import APIRouter, Request, UploadFile, File # pyright: ignore[reportMissingImports]
from fastapi.responses import HTMLResponse # pyright: ignore[reportMissingImports]
from config import ( TEMPLATES, PROFILES_PATH )
from core.utilities.data_lib import ( get_job_categories, project_phases, rate_categories )
from logger import (logger, g_log)
from apps.SiteWorker.worker import ( all_workers, get_worker, save_employee_image  )
from core.utilities.data_lib import ( get_job_categories, project_phases, rate_categories )


router = APIRouter()

def page_url(page:str='')->str:
    return f"/components/employee/{page}"


@lru_cache
@router.get("/index/{filter}")
async def get_workers_index(request:Request, filter:str='all'):
    workers:list = [] 
    workers_index:list = await all_workers()
    if filter != 'all':
        workers = [worker for worker in workers_index if worker.get('value', {}).get('occupation', '') == filter]
    else: 
        workers = workers_index
    return  TEMPLATES.TemplateResponse(
        request=request,
        name=page_url('Index.html'),
        context={            
            "workers": workers,
            "filter": filter,
            "occupation_index": get_job_categories()
        }
    )


@router.get("/{item_id}")
async def read_worker(request:Request, item_id: str, q: str | None = None):
    worker:Employee = await get_worker(id= item_id) # type: ignore

    try:
        result = await update_employee(worker.employee) # type: ignore
        
    except Exception as e:
        logger().exception(e)

    return TEMPLATES.TemplateResponse(
        request=request,
        name= page_url('Employee.html'), 
        context={              
             "employee": worker , 
             "projects": [], #await employee_projects(worker), 
             "occupation_index": get_job_categories()
        }
    )



# Upload worker Profile 
@router.post("/upload_file/{id}")
async def upload_file(request:Request, id:str=''):    
    
    '''if proc == 'employee_image':
            from modules.employee import save_employee_image
            result = await save_employee_image( id=id, upload_file=upload_file )
            return result
        else:
            return JSONResponse(content={"status": "error", "message": "Invalid process type"})
    '''
    worker = await save_employee_image( id=id, request=request )
    try:

        return TEMPLATES.TemplateResponse(
            request=request,
            name= page_url('employeeProfile.html'),
            context={"employee": {"imgurl": worker.imgurl, "oc": worker.oc} }
        )
    except Exception as e:
        logger().exception(e)
        return {"error": str(e)}
    finally:        
        del worker
    