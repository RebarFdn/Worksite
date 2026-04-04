from http import HTTPStatus
from typing import ( Coroutine, Any )
from database.mongo_dms import ( async_client, client)
from database.couch_dms import ( local_db, )
from core.baseModels.employee_models import ( EmployeeModel, )
from core.baseModels.project_models import ( JobModel, Project, ProjectAccount, ProjectWorker )
from core.baseModels.ezchart import (ezChart, )
from core.utilities.utils import ( converTime, convert_timestamp, to_dollars, to_project_id, tally )
from logger import (logger, g_log)

# MongoDB Configuration
database:str = "employee" # The Project Database 
db = async_client.get_database(database)# Database server 

employee_home_collection = db["employee_home"]  # Project base collection

account_collection = db["account"]  # Project jobs collection

job_collection = db["jobs"]  # Project jobs collection

task_collection = db["tasks"]  # Project jobs collection

daywork_collection = db["days"]  # Project jobs collection

report_collection = db["reports"]  # Project jobs collection

# CouchDB Configuration
_databases = { # Employee Databases
            "local":"site-workers", 
            "local_partitioned": False,
            "slave":"site-workers", 
            "slave_partitioned": False
            
            }


# connection to site-projects database 
db_connection:Coroutine = local_db(db_name=_databases.get('local', '')) 


#@lru_cache
async def all_workers(conn:Coroutine=db_connection)->list:
    """_summary_
    Args:
        conn (typing.Coroutine, optional): _description_. Defaults to db_connection.
    Returns:
        list: _description_
    """
    data = await conn.get(_directive="_design/workers/_view/name-index")  # type: ignore
    try:
        return data.get('rows')
    except Exception as e:
        return {"error": str(e)} # type: ignore
    finally: 
        del data


async def get_worker( id:str='', conn:Coroutine=db_connection )->EmployeeModel: 
    """Get a single Employee record by quering the database with employee's _id
    Args:
        id (str, optional): The employee's _id . Defaults to None.
        conn (typing.Coroutine, optional): database connection object. Defaults to db_connection.
    Returns:
        dict: key value store of employee's record.
    """               
    worker:EmployeeModel = EmployeeModel()
    worker.load_data( data= await conn.get(_directive=id) ) # type: ignore
    return worker 


async def update_employee(data:dict={}, conn:Coroutine=db_connection ):
   
    payload = await conn.put( json=data)    # type: ignore
    try:           
        return payload
    except Exception as e:
        return {"error": str(e)}
    finally: 
        del payload
        


