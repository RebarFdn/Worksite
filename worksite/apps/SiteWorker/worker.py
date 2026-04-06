from pathlib import Path
from http import HTTPStatus
from typing import ( Coroutine, Any )
from fastapi import APIRouter, Request, UploadFile, File
from database.mongo_dms import ( async_client, client)
from database.couch_dms import ( local_db, )
from core.baseModels.employee_models import ( EmployeeModel, )
from core.baseModels.project_models import ( JobModel, Project, ProjectAccount, ProjectWorker )
from core.baseModels.ezchart import (ezChart, )
from core.utilities.utils import ( converTime, convert_timestamp, to_dollars, to_project_id, tally, timestamp )
from logger import (logger, g_log)
from config import PROFILES_PATH, system_user


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

#______________________ CRUD Operations for Employee Records ___________________________

## Create Employee Record
async def create_employee(data:dict={}, conn:Coroutine=db_connection )->EmployeeModel | dict:   
    '''Saves a new employee data permanently . Returns the result of the operation'''     
    return await conn.post( json=data) # type: ignore
    
 
## Read Employee Record
async def read_worker( id:str='', conn:Coroutine=db_connection )->EmployeeModel: 
    """Get a single Employee record by quering the database with employee's _id"""
    return await conn.get(_directive=id) # type: ignore
     

## Update Employee Record
async def update_worker(data:dict={}, conn:Coroutine=db_connection ):
    '''Updates an existing employee data permanently . Returns the result of the operation'''   
    return await conn.put( json=data)    # type: ignore
    

## Delete Employee Record
async def delete_worker( id:str='', conn:Coroutine=db_connection ):
    '''Deletes an existing employee data permanently . Returns the result of the operation '''
    return await conn.delete(_id=id)  # type: ignore
    

#_____________  Other Database Operations ___________________________


    

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


async def get_worker(id:str='')->EmployeeModel:
    """_summary_

    Args:
        id (str, optional): _description_. Defaults to ''.

    Returns:
        EmployeeModel: _description_
    """
    employee:EmployeeModel = EmployeeModel()
    try:
        employee.load_data( data= await read_worker(id=id) ) # type: ignore
        return employee
    except Exception as e:
        logger().exception(e)
        return {"error": str(e)} # type: ignore
    finally:
        del employee
    
    

async def save_worker(data:dict={} ):   
    '''Saves a new employee data permanently . Returns the new employee data from database'''  
    employee:EmployeeModel = EmployeeModel()
    employee.load_data( data=data) 
    employee.generate_id  
    employee.metadata.created_by = system_user.username
    employee.metadata.created = timestamp()
    try:        
        result = await create_employee(data=employee.employee) 
        print('CREATE WORKER', result)           
        return employee
    except Exception as e:
        return {"error": str(e)}
    finally:
        del employee
    

async def save_employee_image( request:Request, id:str=''):
    async with request.form() as form: 
        filename:str = form['file'].filename # type: ignore
        contents = await form["file"].read()   # type: ignore

    #img = Image.open(io.BytesIO(contents))
    #print(f"Image verification: {img.tell()}")  # Verify that it is, in fact an image
    #img.close()    
    # update filename to new filename
    new_name = f"{id}.{filename.split('.')[-1]}"  
          
    new_file_path = Path.joinpath(PROFILES_PATH, new_name)
        # convert the image to png format
        # save the image
    with open(new_file_path, "wb") as f:
        f.write(contents)
        
        # open the image
        #img = Image.open(new_file_path)
        # display the image
        #img.show()
        # close the image
        #img.close()

        #update employee data
    worker = await get_worker(id=id)
    worker.imgurl = f"/profile/{new_name}"
    await update_worker( data=worker.employee)
    return worker