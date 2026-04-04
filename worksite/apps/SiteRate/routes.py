# SiteRates Routes
from typing import Any
from fastapi import APIRouter , Request # pyright: ignore[reportMissingImports]
from fastapi.responses import HTMLResponse # pyright: ignore[reportMissingImports]
from config import ( TEMPLATES, system_user)
from core.utilities.data_lib import ( get_job_categories, project_phases, rate_categories )
from logger import (logger, g_log)
from apps.SiteWorker.worker import ( all_workers, get_worker )
from core.utilities.data_lib import ( get_job_categories, project_phases, rate_categories )
from apps.SiteRate.rate import ( all_rates, all_rates_ref, create_rate, delete_rate, get_rate, projects_index , update_rate, save_rate )
from core.baseModels.rate_models import IndustryRateModel


router = APIRouter()

def page_url(page:str='')->str:
    return f"/components/rate/{page}"


@router.get("/index/{filter}")
async def get_rate_index(request:Request, filter:str=''): # type: ignore
    rates_list:list = await all_rates() # type: ignore
    rates:list = []
    for item in rates_list:
        rate:IndustryRateModel = IndustryRateModel() 
        rate.load_data(data=item)
        rates.append(rate)
    
    if filter:
        if filter == 'all' or filter == 'None':            
            irates:list = [rate.rate for rate in rates]
        else:
            irates:list = [rate.rate for rate in rates if rate.category == filter]
    else:
        irates:list = [rate.rate for rate in rates]
    
    try:
        
        return TEMPLATES.TemplateResponse(
            request=request,
            name=page_url('Rates.html'),
            context={
                "filter": filter,
                "rates":  irates,                               
                "categories": {rate.category for rate in rates }, 
                "rate_categories": list(rate_categories().keys())                            
            }
            )
    except Exception as e: 
        logger().exception(e)
    finally: 
        del rates
        del rates_list



## Get a single rate by id
@router.get("/{id}")
async def get_industry_rate(request:Request, id:str=''): # type: ignore
    rate:IndustryRateModel = await get_rate(id=id) # type: ignore
    #print(f"Rate Data: {rate.rate}")
   
    #print(f"Projects: {projects}")
    try:
        return TEMPLATES.TemplateResponse(
            request=request, 
            name=page_url('Rate.html'), 
            context= {                    
                    "rate": rate.rate ,
                    "rate_categories": list(rate_categories().keys()),
                    "projects": await projects_index(), 
                    "shared": False
                }
            )
    except Exception as ex: 
        logger().exception(ex)
        print(f"An error occurred while loading the rate {id}. {str(ex)}")
        #return HTMLResponse(f"<h3>An error occurred while loading the rate {id}.</h3>", status_code=500)

    finally: del rate



@router.post("/save")
async def record_rate_data(request:Request,  user:str=system_user.username):        
        try:
            async with request.form() as form:
                form_data:dict = dict(form)
            return TEMPLATES.TemplateResponse(
            request=request,
            name=page_url('Rate.html'),
            context={
                "rate": await save_rate(form_data=form_data, user=user), # type: ignore , 
                "rate_categories": list(rate_categories().keys()),
                "projects": await projects_index(), 
                "shared": False
            }
        )                             
        except Exception as e: 
            logger().exception(e)
            return {"error": str(e)}
'''

## Clone an existing rate and save the clone to the database
async def clone_industry_rate(request:Request, id:str='')->TEMPLATES.TemplateResponse:
    categories = rate_categories()
    clone:IndustryRateModel = IndustryRateModel()
    async with request.form() as form:
        form_data:dict = dict(form)
    if form_data.get('title') and form_data.get('description'):
        clone.load_form_data(form_data=form_data)
    else:
        clone.load_data(data=await get_industry_rate(request, id=id))
    clone.generate_id
    clone.set_cloned(cloned_from=id)
    try:
        await create_rate(data=clone.rate)   
        notice(
        title="Industry Rate Action - Cloning",
        message=f"Industry Rate {clone.rate.get('title')} has been cloned from {id}."
        )    
        return TEMPLATES.TemplateResponse(page_url('RateConsole.html'), 
                {"request": request, "rate": clone.rate ,"rate_categories": list(categories.keys()), "shared": False}
            )
    except Exception as e: 
        logger().exception(e)
    finally: 
        del clone
        del categories
        del form_data


async def update_industry_rate(request:Request, id:str='')->TEMPLATES.TemplateResponse: 
    categories = rate_categories()
    async with request.form() as form:
        form_data:dict = dict(form)    
    rate:IndustryRateModel = IndustryRateModel() 
    rate.load_data(data=await get_industry_rate(request, id=id))   
    rate.load_form_data(form_data=form_data)  
    ## Update        
   
    await update_rate(data=rate.rate)
    notice(
        title="Industry Rate Update Action",
        message=f"Industry Rate {rate.title} has been updated."    )

    return TEMPLATES.TemplateResponse(page_url('RateConsole.html'), 
                {"request": request, "rate": rate.rate ,"rate_categories": list(categories.keys()), "shared": False}
            )


async def backup_industry_rate(data:dict={}, conn:typing.Coroutine=db_connection)->dict:      
    """restores and existing  Rate Item Permanently on the Platform."""    
    new_rate:dict = rate_model() | data
    try:
        await conn.post(json=new_rate) 
        return new_rate
    except Exception as e: logger().exception(e)  
    finally: del new_rate

'''

