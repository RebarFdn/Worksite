from typing import ( Any )
from fastapi import APIRouter , Request # pyright: ignore[reportMissingImports]
from fastapi.responses import HTMLResponse, StreamingResponse # pyright: ignore[reportMissingImports]
from config import (STATIC_PATH, TEMPLATES, TEMPLATES_PATH)
from apps.SiteProject.project import ( create_project, read_project, delete_project, get_jobs, get_workers , get_worker, all_projects, suppliers, account_statistics, piechart, update_project, Project, JobModel )
from apps.SiteRate.rate import ( all_rates )
from apps.SiteProject.analytics import (IncomeDataFrame)
from core.utilities.data_lib import ( project_phases, rate_categories )
from logger import (logger, g_log)


router = APIRouter()


@router.get("/index")
async def get_project_index(request:Request):
    return TEMPLATES.TemplateResponse( request=request, name="index.html", context={'title': 'Projects','projects': await all_projects()})


@router.get("/projects")
async def index_home(request:Request):

    return TEMPLATES.TemplateResponse( request=request, name="components/project/index.html", context={'title': 'Projects','projects': await all_projects()})


@router.post("/project/")
async def save_project(data:dict={}):
    result = create_project(data=data)
    return {"Project": result}


@router.get("/project/{item_id}")
async def read_item(request:Request, item_id: str, q: str | None = None):
    project:Project = await read_project(id= item_id) # type: ignore
    return TEMPLATES.TemplateResponse( 
        request=request,        
        name="components/project/ProjectPage.html", 
        context={
            'title': 'Projects',
            'project':project.project,
            "suppliers":suppliers,                    
            "project_phases": project_phases(),
            "rate_categories": rate_categories().keys()

        }
    )


@router.delete("/project/{item_id}")
async def delete_item(item_id: str, q: str | None = None):
    return delete_project(id= item_id)


# Project Home Routes
@router.get("/home/{project_id}")
async def read_home(request:Request, project_id: str, q: str | None = None):
    project:Project = await read_project(id= project_id) # type: ignore
    project.load_jobs()
    project.load_account()    
    return TEMPLATES.TemplateResponse( 
         request=request, 
        name="components/project/Home.html", 
        context={
            'title': 'Home',
            'project':project.project,
            "suppliers":suppliers,                    
            "project_phases": project_phases(),
            "rate_categories": rate_categories().keys()

        }
        
    )



# Project Accounting Routes
@router.get("/account/{project_id}")
async def read_account(request:Request, project_id: str, q: str | None = None):
    project:Project = await read_project(id= project_id) # type: ignore
    project.load_jobs()
    project.load_account()    
    return TEMPLATES.TemplateResponse( 
        request=request, 
        name="components/project/account/Account.html", 
        context={
            'title': 'Project Account Page',
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


@router.get("/paybill/{project_id}/{bill_id}")
async def read_paybill(request:Request, project_id: str, bill_id: str ,q: str| None = None):
    project:Project = await read_project(id= project_id) # type: ignore
    #project.load_jobs()
    project.load_account() 
    project.load_workers()
    paybill = project.account.get_paybill(id=bill_id)
    
    return TEMPLATES.TemplateResponse( 
        request=request, 
        name="components/project/account/PayBill.html", 
        context={
            'title': 'Project Account Paybill',
            'project': {
                    "name": project.name, 
                    "workers": project.workers, 
                    "labour_cost": project.project_labour_cost,
                    "state": project.state,                    
                    },
            "paybill": paybill,
            "unpaid_tasks": [],
            "items_tally": [ item.model_dump() for item in paybill.items ], # type: ignore
            "supplier_filter": list(set(invoice.supplier.name for invoice in project.account.records.invoices)),
            "suppliers": suppliers,
            "invoice_filter": 'all'
            
        }
        
    )
    
    

@router.get("/stats/{project_id}")
async def read_account_statistics(request:Request, project_id: str):
    project:Project = await read_project(id= project_id) # type: ignore
    project.load_jobs()
    project.load_account()
    return TEMPLATES.TemplateResponse( 
        request=request, 
        name="components/project/account/Statistics.html", 
        context={
            "project": await account_statistics( project_id=project_id )
        }
    )



@router.get("/piechart/{project_id}")
async def read_piechart(request:Request, project_id: str)-> HTMLResponse:
    chart:ezChart = await piechart(project_id=project_id) # type: ignore
    return HTMLResponse(content=chart.chart(), status_code=200)


@router.get("/heatmap/{project_id}")
async def read_heatmap(request:Request, project_id: str)-> HTMLResponse:
    project:Project = await read_project(id= project_id) # type: ignore
    project.load_jobs()
    project.load_account()
    frame:IncomeDataFrame= IncomeDataFrame()
    frame.load_data( project.account.transactions.deposit) 
    map = frame.heatMap()   
    return HTMLResponse(map)
   

@router.get("/deposit_histogram/{project_id}")
async def deposit_hist(request:Request, project_id: str)-> HTMLResponse:
    project:Project = await read_project(id= project_id) # type: ignore
    project.load_jobs()
    project.load_account()
    frame:IncomeDataFrame= IncomeDataFrame()
    frame.load_data( project.account.transactions.deposit) 
    #print(project.account.transactions.deposit)
    
    return HTMLResponse(frame.deposit_histogram())


@router.get("/deposit_calendar/{project_id}")
async def deposit_calendar(request:Request, project_id: str)-> StreamingResponse:
    project:Project = await read_project(id= project_id) # type: ignore
    project.load_jobs()
    project.load_account()
    frame:IncomeDataFrame= IncomeDataFrame()
    frame.load_data( project.account.transactions.deposit) 
    calendars:list = frame.calendars
    def generate_stream(cal:list):
        yield f"""<div uk-grid>"""
        for item in cal:
            yield f"<div>{item}</div>"
        yield "</div>"

    return StreamingResponse(content=generate_stream(calendars))
                
   




@router.get("/workers/{project_id}")
async def get_project_workers(request:Request, project_id:str):
    project:Project = await read_project(id= project_id) # type: ignore
    project.load_workers()
    
    return TEMPLATES.TemplateResponse(
            request=request, 
            name= '/components/project/worker/Workers.html', 
            context= {   
                'title': 'Workers',                 
                    "project":  {
                        "_id": project.id, 
                        "state": project.state, 
                        "workers": project.workers,
                        "employees": [] #project.employees
                        }
                })



@router.get("/worker/")
def get_project_worker(request:Request, project_id:str, worker_id:str):
    return get_worker( project_id=project_id, worker_id=worker_id)



@router.get("/jobs/{project_id}")
async def get_project_jobs(request:Request, project_id:str):
    project:Project = await read_project(id= project_id) # type: ignore
    project.load_jobs()
    #project.load_rates()
    #print("Project Jobs Data:", project.jobs)
    return  TEMPLATES.TemplateResponse(
        request=request, 
        name= '/components/project/job/Jobs.html', 
        context= {   
            'title': 'Jobs',                 
                    "project": {
                        '_id': project.id,                       
                        'state': project.state,
                        'jobs': project.jobs,
                        #'rates': project.rates,
                        #'industry_rates': [], #project.industry_rates,
                        #'rate_categories': rate_categories().keys()
                    }
        })

'''
## Get a Job | DONE
@router.get("/job/{project_id}")
async def get_project_job(request:Request, project_id:str='' ): # type: ignore
    project:Project = await read_project(id= project_id) # type: ignore
    project.load_jobs()
    project.load_rates()
    project.load_workers()
    job_id:str=''
    job:JobModel = project.get_job(job_id=job_id)
    filter:set = set( task.category for task in job.tasks if task.category)        
    try:            
        return TEMPLATES.TemplateResponse(
            request=request, 
            name= '/components/project/job/Job.html', 
            context={                     
                    "project": { 
                        "_id": project.id,
                        "rates": [ rate.model_dump() for rate in project.rates ],
                        "workers": [ worker.model_dump() for worker in project.workers ],
                        "jobs":[{"id": job.id, "title": job.title} for job in project.jobs]
                        
                        },
                    "job": job.model_dump(),                    
                    "filter": filter
                }
            )
    except Exception as e:
        logger().exception(e)
        #notice(title="Job request Error.", message=f"The request for Job {job_id} was not processed.")
    finally:                
        del(project) # clean up
        del(job)
        

'''

# Project Daywork Routes
@router.get("/dayswork/{project_id}")
async def read_dayswork(request:Request, project_id: str, q: str | None = None):
    project:Project = await read_project(id= project_id) # type: ignore
    project.load_dayswork()
    project.load_workers()    
    return TEMPLATES.TemplateResponse( 
         request=request, 
        name="components/project/daywork/Days.html", 
        context={
            'title': 'Dayswork',
            'project':project,
            "suppliers":suppliers,                    
            "project_phases": project_phases(),
            "rate_categories": rate_categories().keys()

        }
        
    )



# Project Rate Routes
@router.get("/rates/{project_id}/{filter}")
async def read_rates( request:Request, project_id: str, filter: str = 'all' ):
    project:Project = await read_project( id= project_id ) # type: ignore
    project.load_rates()
    industry_rates:Any = await all_rates()
    project.load_industry_rates( rates_list= industry_rates )
    #project.load_workers()    
    return TEMPLATES.TemplateResponse( 
         request=request, 
        name="components/project/Rates.html", 
        context={
            'title': 'Rates',
            'project':project,
            "suppliers":suppliers,                    
            "project_phases": project_phases(),
            "rate_categories": rate_categories().keys()

        }
        
    )
    
# MAterials Inventory
@router.get("/inventory/{project_id}")
async def read_inventory( request:Request, project_id: str, q: str = 'all' ):
    project:Project = await read_project( id= project_id ) # type: ignore
    project.load_inventories()     
    return TEMPLATES.TemplateResponse( 
         request=request, 
        name="components/project/inventory/Inventories.html", 
        context={
            'title': 'Materials Inventory',
            'project': { 
                "_id": project.id,
                "inventories": project.inventories,
                "state": project.state
            }           
        }        
    )
    
# Event State 
@router.get("/events/{project_id}")
async def read_event_state( request:Request, project_id: str, q: str = 'all' ):
    project:Project = await read_project( id= project_id ) # type: ignore
      
    return TEMPLATES.TemplateResponse( 
         request=request, 
        name="components/project/event_state/eventState.html", 
        context={
            'title': 'Project Event and State',
            'project': { 
                "_id": project.id,
                "event": project.event,
                "state": project.state,
                "metadata": project.metadata
            }           
        }        
    )
 
 
# Update state    
@router.post("/state/{project_id}/{state}")
async def process_state_event( request:Request, project_id: str, state: str | None = None ):
    project:Project = await read_project( id= project_id ) # type: ignore
    print(f"Request to update: {state}")
    if state:
        project.update_state(state=state)
    
        await update_project(data=project.project)
    return TEMPLATES.TemplateResponse( 
         request=request, 
        name="components/project/event_state/eventState.html", 
        context={
            'title': f'Updated Project Event and State {state}',
            'project': { 
                "_id": project.id,
                "event": project.event,
                "state": project.state,
                "metadata": project.metadata
            }           
        }        
    )
    
       
# Activity Logs 
@router.get("/activity_logs/{project_id}")
async def read_activity_logs( request:Request, project_id: str, q: str = 'all' ):
    project:Project = await read_project( id= project_id ) # type: ignore
    project.load_logs      
    return TEMPLATES.TemplateResponse( 
         request=request, 
        name="components/project/ActivityLogs.html", 
        context={
            'title': 'Project Event Logs',
            'project': { 
                "_id": project.id,
                "activity_logs": project.activity_logs               
            }           
        }        
    )
 