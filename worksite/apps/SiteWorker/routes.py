# SiteWorker Routes
from typing import Any
from fastapi import APIRouter , Request # pyright: ignore[reportMissingImports]
from fastapi.responses import HTMLResponse # pyright: ignore[reportMissingImports]
from config import ( TEMPLATES, )
from core.utilities.data_lib import ( get_job_categories, project_phases, rate_categories )
from logger import (logger, g_log)
from apps.SiteWorker.worker import ( all_workers, get_worker )
from core.utilities.data_lib import ( get_job_categories, project_phases, rate_categories )


router = APIRouter()

def page_url(page:str='')->str:
    return f"/components/employee/{page}"


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
    return TEMPLATES.TemplateResponse(
        request=request,
        name= page_url('Employee.html'), 
        context={              
             "employee": worker , 
             "projects": [], #await employee_projects(worker), 
             "occupation_index": get_job_categories()
        }
    )