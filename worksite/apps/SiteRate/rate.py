# SiteRates Module
from http import HTTPStatus
from typing import ( Coroutine, Any )
import typing
from database.mongo_dms import ( async_client, client)
from database.couch_dms import ( local_db, )
from core.baseModels.rate_models import ( IndustryRateModel, )
from core.baseModels.project_models import ( JobModel, Project, ProjectAccount, ProjectWorker )
from core.baseModels.ezchart import (ezChart, )
from core.utilities.utils import ( converTime, convert_timestamp, timestamp, to_dollars, to_project_id, tally )
from logger import (logger, g_log)
from config import system_user
from apps.SiteProject.project import ( all_projects, ) 
                                      

# MongoDB Configuration
database:str = "rates" # The Rates Database 
db = async_client.get_database(database)# Database server
rate_collection = db["rate_sheet"]  # Project base collection

# CouchDB Configuration
_databases:dict = { # industry rate Databases
            "local":"rate-sheet", 
            "local_partitioned": False,
            "slave":"rate-sheet", 
            "slave_partitioned": False,
            "projects":"lite-projects",            
            }
# connection to Industry rate sheets database 
db_connection:Coroutine = local_db(db_name=_databases.get('local', '')) 
# connection to site-projects database 
projects_db_connection:Coroutine = local_db(db_name=_databases.get('projects', ''))  


def page_url(page:str='')->str:
    return f"/components/rate/{page}"
user = system_user.username
# ________________________________________________________________________________


# Project Id Index
async def projects_index()->list:
    """Returns:
        list: _description_
    """
    return [{"_id": project.get('id'), "name": project.get('name')} for project in await all_projects()]

# CRUD Functions for Industry Rates
# CREATE a new rate
 
# Stores a new rate to the database
async def create_rate(data:dict={}, conn:Coroutine=db_connection)->dict: 
    try:        
        await conn.post(json=data)  # type: ignore
        return data
    except Exception as e: 
        logger().exception(e) 
        return data 
    finally: del data


# READ functions for Industry Rates
## Get a single rate by id
async def get_rate(id:str, conn:typing.Coroutine=db_connection)->IndustryRateModel | None :
    rate:IndustryRateModel = IndustryRateModel()
    rate.load_data(data=await conn.get(_directive=id))  # type: ignore
    try:
        return rate
    except Exception: logger().exception(Exception)
    finally: del rate
 

## Get Rate ID and Revision Index
async def all_rates_ref(conn:typing.Coroutine=db_connection)->list | None:
    rates:dict = await conn.get(_directive = "_all_docs")    # type: ignore
    try:            
        return  rates.get('rows')        
    except Exception as e: logger().exception(e)
    finally: del rates


## Get Rates List Index
async def all_rates(conn:typing.Coroutine=db_connection)->list | None: 
        '''Retreives a list of rate data.
        ''' 
        r = None      
        def processrates(rate):
            return rate['value']            
        try:
            r = await conn.get(_directive="_design/index/_view/document") # type: ignore
            return list(map(processrates,  r.get('rows', []) ))
        except Exception as e: logger().exception(e)
        finally: del(r)

# UPDATE functions for Industry Rates

## Update an existing rate
async def update_rate(data:dict={}, conn:typing.Coroutine=db_connection):
    '''Updates a Rate Item with data provided.
    --- Footnote:
            enshure data has property _id
    extra:
        updates the objects meta_data property 
        or create and stamp the meta_data field
        if missing                 
    '''
    if '_rev' in list(data.keys()): del(data['_rev'])      
    try: return await conn.put(json=data)             # type: ignore
    except Exception as e: logger().exception(e)
        
# DELETE functions for Industry Rates
async def delete_rate(id:str='', conn:typing.Coroutine=db_connection):
        '''Permanently Remove a Rate Item from the Platform.
        ---Requires:
            name: _id
            value: string 
            inrequest_args: True
        '''        
        try: return await conn.delete(_id=id) # type: ignore
        except Exception as e: logger().exception(e)

# Rate Item Action Functions

## Save a new rate to the database
async def save_rate(form_data:dict, cloned:str='', user:str=user,)->IndustryRateModel | dict:
    '''Stores a Rate Item Permanently on the Platform.'''
    new_rate:IndustryRateModel = IndustryRateModel()
    new_rate.load_form_data(form_data=form_data)
    new_rate.metadata.created_by = user
    new_rate.metadata.created = timestamp()
    #new_rate.set_cloned(cloned_from=cloned)
    try:   
        await create_rate(data=new_rate.rate)
        return new_rate
    except Exception as ex:
        g_log.exception(str(ex))
        return {"error": str(ex)}
    finally:
        del new_rate
        del form_data


