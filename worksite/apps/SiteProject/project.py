from http import HTTPStatus
from typing import ( Coroutine, Any )
from database.mongo_dms import ( async_client, client)
from database.couch_dms import ( local_db, )
from core.baseModels.project_models import ( Project, )
from core.utilities.utils import converTime, convert_timestamp, to_dollars, to_project_id, tally

# MongoDB Configuration
database:str = "project" # The Project Database 
db = client.get_database(database)# Database server 

project_home_collection = db["project_home"]  # Project base collection
workers_collection = db["workers"]  # Project workers collection
job_collection = db["jobs"]  # Project jobs collection
rate_collection = db["rates"]  # Project jobs collection
daywork_collection = db["dayswork"]  # Project jobs collection
inventory_collection = db["inventory"]  # Project jobs collection
account_collection = db["accounts"]  # Project jobs collection
estimate_collection = db["estimates"]  # Project jobs collection
report_collection = db["reports"]  # Project jobs collection
logs_collection = db["activity_logs"]  # Project jobs collection



# CouchDB Configuration
_databases:dict = { # Project Databases
            "local":"lite-projects", 
            "local_partitioned": False,
            "slave":"lite-projects", 
            "slave_partitioned": False ,
            "invoice_db": "temp_invoice"           
            }
# connection to site-projects database 
db_connection:Coroutine = local_db(db_name=_databases.get('local', '')) 

suppliers: list = [ ] #item.get('name') for item in await supplier_name_index()]

# Project CRUD operations 
def crunch_data(id:str,flag:str, data:Any=None):
    return {
        "_id": id,
        flag: data

    }


def save_project(data:dict={}):
    project:Project = Project()
    project.load_data( data=data )
    try:
        workers = crunch_data(id=data.get('_id', ''), flag='workers', data=data.get('workers', []))
        result = {
            "project": project_home_collection.insert_one( project.project ),
            "workers": workers_collection.insert_one( workers ),
            "jobs": job_collection.insert_one( crunch_data(id=data.get('_id', ''), flag='jobs', data=data.get('jobs', [])) ),
            "rates": rate_collection.insert_one( crunch_data(id=data.get('_id', ''), flag='rates', data=data.get('rates', [])) ),
            "dayswork": daywork_collection.insert_one( crunch_data(id=data.get('_id', ''), flag='dayswork', data=data.get('dayswork', [])) ),
            "inventory": inventory_collection.insert_one( crunch_data(id=data.get('_id', ''), flag='inventory', data=data.get('inventory', [])) ),
            "accounts": account_collection.insert_one( crunch_data(id=data.get('_id', ''), flag='accounts', data=data.get('accounts', [])) ),
            "estimates": estimate_collection.insert_one( crunch_data(id=data.get('_id', ''), flag='estimates', data=data.get('estimates', [])) ),
            "reports": report_collection.insert_one( crunch_data(id=data.get('_id', ''), flag='reports', data=data.get('reports', [])) ),
            "logs": logs_collection.insert_one( crunch_data(id=data.get('_id', ''), flag='logs', data=data.get('logs', [])) )
        }
        print(result)

        return 
    except Exception as ex:
        print( str(ex))
    finally:
        #print("PROJECT", project)
        del project


## Create Project
def create_project( data:dict={} ):
    project:Project = Project()
    project.load_data( data=data )
    try:
        result = project_home_collection.insert_one( project.project )
        return result
    except Exception as ex:
        print( str(ex))
    finally:
        #print("PROJECT", project)
        del project


## Read Project
async def read_project(id:str='', conn:Coroutine=db_connection):

    project:Project = Project()
    try:
        data:dict = project_home_collection.find_one({"_id": id}) # type: ignore
        #print(data)
        #project:Project = Project( **data ) # type: ignore
        project.load_data( data=data )
        #project_data:dict = await conn.get(_directive=id) # type: ignore        
        #project.load_data(data=project_data  )
        #project.load_workers()
        #project.load_jobs()
        #project.load_rates()
        #save_project(data=project_data)
        return project.project
    except Exception as ex:
        return {'error': str(ex) } #HTTPStatus(404).description}


## Update Project
def update_project(data:dict={}, conn:Coroutine=db_connection):
    query_filter = {'_id' : data.get('_id')}
    update_operation = { '$set' : data }
    result = project_home_collection.update_one(query_filter, update_operation)    
    try:  
        print(result)     
        
        return read_project(id=data.get('_id', ''))
    except Exception as ex:
        return {'error': str(ex) } #HTTPStatus(404).description}
    finally:
        del query_filter
        del update_operation
        del result


## Delete Project   
async def all_projects(conn:Coroutine=db_connection ) -> list[dict]:
    data:dict = await conn.get(_directive="_design/project-index/_view/name-view")  # type: ignore
    
    projects_couch:list[dict] = [{"id": doc.get('id'), "name": doc.get('key'), "description": f"{doc.get('value').get('category')} project started on { converTime(doc.get('value').get('metadata', {}).get('created'))}"} for doc in data.get('rows', []) ]
    #projects_mongo = [{"id": doc.get('_id'), "name": doc.get('name'), "description": f"{doc.get('category')} project started on { converTime(doc.get('event', {}).get('started'))}"} for doc in project_home_collection.find() ]
    return projects_couch # type: ignore


## Delete Project   
def delete_project(id:str='', conn:Coroutine=db_connection):
    return project_home_collection.delete_one( {"_id": id} )

# Project Worker Management

## Add worker to project workers
def get_worker(project_id:str='', worker_id:str=''):
    
    try:
        result = workers_collection.find_one({"_id": project_id})
    
        return [ worker for worker in result.get('workers') if worker.get('key') == worker_id ][0] # type: ignore
    except Exception as ex:
        return {'error': str(ex) } #HTTPStatus(404).description}


    
def get_workers(project_id:str=''):
    
    try:
        result = workers_collection.find_one({"_id": project_id})
    
        return result
    except Exception as ex:
        return {'error': str(ex) } #HTTPStatus(404).description}

