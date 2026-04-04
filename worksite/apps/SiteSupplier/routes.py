# Supplier Routes
from typing import Any, Coroutine
from fastapi import APIRouter , Request # pyright: ignore[reportMissingImports]
from fastapi.responses import HTMLResponse
from pycountry import db # pyright: ignore[reportMissingImports]
from config import ( TEMPLATES, system_user)
from core.utilities.utils import ( timestamp )
from core.utilities.data_lib import ( get_job_categories, project_phases, rate_categories )
from logger import (logger, g_log)
from apps.SiteSupplier.supplier import ( all_suppliers, read_supplier, supplier_by_name, update_supplier, delete_supplier ,all_suppliers_ref, suppliers_name_index , suppliers_index, save_supplier)
from core.baseModels.supplier_models import Supplier


router = APIRouter()

def page_url(page:str='')->str:
    return f"/components/supplier/{page}"
  

@router.get("/index/{filter}")
async def get_supplier_index(request:Request, filter: str = 'all'): # type: ignore    
    try:        
        return TEMPLATES.TemplateResponse(
            request=request,
            name=page_url('Index.html'),
            context= await suppliers_index(filter=filter) # type: ignore
        )
    except Exception as e: 
        logger().exception(e)
        return HTMLResponse(content=f"<h1>Error: {str(e)}</h1>", status_code=500)
    


@router.get("/{id}")
async def get_supplier_page(request:Request, id:str=''): # type: ignore
    supplier:Supplier = await read_supplier(id=id) # type: ignore
    try:
        return TEMPLATES.TemplateResponse(
            request=request,
            name=page_url('Supplier.html'),
            context={
                "supplier": supplier, 
                "total_transactions": 0.00  # Placeholder for total transactions, to be calculated from supplier's transaction history              
            }
        )
    except Exception as e: 
        logger().exception(e)
        return HTMLResponse(content=f"<h1>Error: {str(e)}</h1>", status_code=500)
    finally: del(supplier)
        

@router.post("/save")
async def record_supplier_data(request:Request,  user:str=system_user.username):        
        try:
            async with request.form() as form:
                form_data:dict = dict(form)
            return TEMPLATES.TemplateResponse(
            request=request,
            name=page_url('Supplier.html'),
            context={
                "supplier": await save_supplier(form_data=form_data, user=user), # type: ignore , 
                "total_transactions": 0.00  # Placeholder for total transactions, to be calculated from supplier's transaction history              
            }
        )
        
                             
        except Exception as e: 
            logger().exception(e)
            return {"error": str(e)}