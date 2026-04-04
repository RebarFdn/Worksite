# Supplier Module
from http import HTTPStatus
from typing import ( Coroutine, Any )
from database.mongo_dms import ( async_client, client)
from database.couch_dms import ( local_db, )
from core.baseModels.supplier_models import ( Supplier, MaterialSupplier)
from core.baseModels.project_models import ( JobModel, Project, ProjectAccount, ProjectWorker )
from core.baseModels.ezchart import (ezChart, )
from core.utilities.utils import ( converTime, convert_timestamp, timestamp, to_dollars, to_project_id, tally )
from logger import (logger, g_log)

# MongoDB Configuration
database:str = "supplier" # The Project Database 
db = async_client.get_database(database)# Database server 
supplier_home_collection = db["suppliers"]  # Project base collection
transactions_collection = db["transactions"]  # Project jobs collection


# CouchDB Configuration
_databases = { # Suppliers Databases
            "local":"site-suppliers", 
            "local_partitioned": False,
            "slave":"site-suppliers", 
            "slave_partitioned": False            
            }


# connection to site-projects database 
db_connection:Coroutine = local_db(db_name=_databases.get('local', '')) 


def page_url(page:str='')->str:
    return f"/components/supplier/{page}"


#____________________ CRUD Operations ____________________
 
## Create or Update Supplier
async def create_supplier(data:dict, user:str='', conn:Coroutine=db_connection): 
    
    try:
        result = await conn.post( json=data)   # type: ignore
        return result                   
    except Exception as e: 
        logger().exception(e)
        return {"error": str(e)}
    


## Read Supplier by Id
async def read_supplier( id:str='', conn:Coroutine=db_connection)->Supplier | dict:
    r:dict = {}
    supplier:Supplier = Supplier()
    try:
        supplier.load_data(data=await conn.get(_directive=id)) # type: ignore
        return supplier
    except Exception as e: 
        logger().exception(e)
        return {"error": str(e)}

    finally: 
        del(r)
        del supplier


## Update Supplier
async def update_supplier( data:dict={}, conn:Coroutine=db_connection)->dict:          
    try:        
        result = await conn.put(json=data)  # type: ignore
        return result           
    except Exception as e:
        logger().exception(e)
        return {"error": str(e)}
    

## Delete Supplier
async def delete_supplier( id:str='', conn:Coroutine=db_connection ):
    try: return await conn.delete(_id=id)            # type: ignore
    except Exception as e: logger().exception(e)

#____________________ DATABASE INDEX  Operations ____________________


## Get All Suppliers Ids and _revisions ids.
async def all_suppliers_ref(conn:Coroutine=db_connection)->list:
    result:dict = await conn.get(_directive="_all_docs") # type: ignore
    try:
        return result.get('rows', [])           
    except Exception as ex: 
        logger().exception(ex)
        return []
    finally: del(result)

## Get All Suppliers Data.
async def all_suppliers(conn:Coroutine=db_connection)->list:
    result:dict = await conn.get(_directive="_design/suppliers/_view/all") # type: ignore
    try:         
        return result.get('rows', [])           
    except Exception as e: 
        logger().exception(e)
        return []
    finally: del(result)

## Get Supplier Index by name
async def suppliers_name_index(conn:Coroutine=db_connection)->list:
    def processIndex(p): 
        return p.get('key')
    result:dict = await conn.get(_directive="_design/suppliers/_view/name-index")  # type: ignore
    try:       
        return list(map( processIndex,  result.get('rows', [])))            
    except Exception as ex: 
        logger().exception(ex)
        return []
    finally: del(result)

## Get Supplier Index by invoice id
async def suppliers_invoice_id_index(conn:Coroutine=db_connection)->list: # type: ignore
    def processIndex(p): 
        return  p.get('key')
    r:dict = {}
    try:
        r = await conn.get(_directive="_design/project-index/_view/invoice-id")  # type: ignore
        return list(map( processIndex,  r.get('rows', [])))            
    except Exception as e: logger().exception(e)
    finally: del(r)

# ___________________ Data REQUEST Operations _____________


### Get Supplier Name:Id Index 
async def supplier_key_index()->dict:
    index =  await suppliers_name_index()
    return {item.get('name').strip(): item.get('_id') for item in index }
    

### Get Supplier by name
async def supplier_by_name(name:str='')->Supplier | dict: # type: ignore
    index = await suppliers_name_index()
    try:
        for item in index:
            if item.get('name').strip() == name:
                break
            return await read_supplier(id=item.get('_id'))
    except Exception as e:
        logger().exception(e)
        return {"error": str(e)}
    finally: del(index)

   
### Get Filtered Suppliers Index
async def suppliers_index(filter: str = 'all'): # type: ignore
    all_suppliers = await suppliers_name_index() # type: ignore
    suppliers = None   
    try:
        if filter == 'all' or filter == 'None':            
            suppliers = all_suppliers
        else:
            suppliers= [supplier for supplier in all_suppliers if supplier.get("address").get("city_parish") == filter ]
        
        return {                        
            "suppliers": suppliers,
            "filter": filter,
            "locations": {supplier.get("address").get("city_parish") for supplier in all_suppliers }            
            }
        
    except Exception as e: 
        logger().exception(e)
        return {"error": str(e)}
    finally: 
        del suppliers
        del all_suppliers
    

    
async def save_supplier(form_data:dict, user:str='', conn:Coroutine=db_connection)->Supplier | dict:
    supplier:Supplier = Supplier()
    try:
        supplier.load_form_data(form_data=form_data)
        supplier.generate_id
        supplier.metadata.created= timestamp()
        supplier.metadata.created_by = user    
        await conn.post( json=supplier.supplier )   # type: ignore
        return supplier                      
    except Exception as e: 
        logger().exception(e)
        return {"error": str(e)}
    finally:
        del supplier
