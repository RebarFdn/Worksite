from http import HTTPStatus
from database.mongo_dms import ( async_client, client)
from project_models import ( Project, )

database:str = "project" # The Project Database 

db = client.get_database(database)# Database server 

project_home_collection = db["project_home"]  # Project base collection
workers_collection = db["workers"]  # Project workers collection

# Project CRUD operations 

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
def read_project(id:str=''):
    project:Project = Project()
    try:
        data:dict = project_home_collection.find_one({"_id": id}) # type: ignore
        project.load_data(data=data  )
        #project.load_workers()
        #project.load_jobs()
        #project.load_rates()
        return project
    except Exception as ex:
        return {'error': str(ex) } #HTTPStatus(404).description}

## Update Project
def update_project(data:dict={}):
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
def all_projects():
    return [{"id": doc.get('_id'), "name": doc.get('name')} for doc in project_home_collection.find() ]

## Delete Project   
def delete_project(id:str=''):
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

