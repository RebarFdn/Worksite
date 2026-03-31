from fastapi import APIRouter , Request # pyright: ignore[reportMissingImports]
from fastapi.responses import HTMLResponse # pyright: ignore[reportMissingImports]
from config import (STATIC_PATH, TEMPLATES, TEMPLATES_PATH)


from apps.SiteProject.project import ( create_project, read_project, delete_project, get_workers , get_worker, all_projects, suppliers, account_statistics, Project)

from core.utilities.data_lib import ( get_job_categories, project_phases, rate_categories )


router = APIRouter()


@router.get("/projects")
async def index_home(request:Request):

    return TEMPLATES.TemplateResponse( request=request, name="components/project/index.html", context={'projects': await all_projects()})


@router.post("/project/")
async def save_project(data:dict={}):
    result = create_project(data=data)
    return {"Project": result}


@router.get("/project/{item_id}")
async def read_item(request:Request, item_id: str, q: str | None = None):
    project:Project = await read_project(id= item_id)
    return TEMPLATES.TemplateResponse( 
        request=request, 
        name="components/project/ProjectPage.html", 
        context={
            'project':project.project,
            "suppliers":suppliers,                    
            "project_phases": project_phases(),
            "rate_categories": rate_categories().keys()
        }
    )


@router.delete("/project/{item_id}")
async def delete_item(item_id: str, q: str | None = None):
    return delete_project(id= item_id)


# Project Accounting Routes
@router.get("/account/{project_id}")
async def read_account(request:Request, project_id: str, q: str | None = None):
    project:Project = await read_project(id= project_id)
    project.load_jobs()
    project.load_account()

    return TEMPLATES.TemplateResponse( 
        request=request, 
        name="components/project/account/Account.html", 
        context={
            'project': {
                    "_id": project.id, 
                    "account": project.account, 
                    "labour_cost": project.project_labour_cost,
                    "state": project.state,                    
                    },
            "tax_tally": sum([ invoice.tax for invoice in project.account.records.invoices ]),
            "supplier_filter": list(set(invoice.supplier.name for invoice in project.account.records.invoices)),
            "suppliers": suppliers,
            "invoice_filter": 'all'
        }
        
    )


@router.get("/stats/{project_id}")
async def read_account_statistics(request:Request, project_id: str):
    project:Project = await read_project(id= project_id)
    project.load_jobs()
    project.load_account()

    return TEMPLATES.TemplateResponse( 
        request=request, 
        name="components/project/account/Statistics.html", 
        context={
            "project": await account_statistics( project_id=project_id )
        }
    )


@router.get("/workers/{project_id}")
async def get_project_workers(project_id:str):
    return get_workers(project_id= project_id)


@router.get("/worker/")
def get_project_worker(project_id:str, worker_id:str):
    return get_worker( project_id=project_id, worker_id=worker_id)



@router.get("/index")
async def get_project_index(request:Request):
    return TEMPLATES.TemplateResponse( request=request, name="index.html", context={'projects': await all_projects()})


