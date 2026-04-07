from apps.SiteProject.project import ( create_project, read_project, delete_project, get_workers , get_worker, all_projects, get_account)
from apps.SiteWorker.worker import ( all_workers, get_worker )
from asyncio import run
from apps.SiteSupplier.supplier import (all_suppliers, get_supplier, get_supplier_by_name, save_supplier, delete_supplier ,all_suppliers_ref, supplier_name_index )

def test_all_projects():
    result = all_projects()
    assert isinstance(result, list) 
    #print("All Projects:", result)

def test_get_account():
    
    result = get_account(project_id="KS03093") # type: ignore
    assert result is not None
    print( result)

#test_all_projects()
#test_get_account()

async def test_all_workers():
    result = await all_workers()
    assert isinstance(result, list) 
    print("All Workers:", result)   


async def test_get_worker():
    result = await get_worker(id="AG37282") # type: ignore
    assert result is not None
    #print( result.address)
    for item in result.address:
        key, val = item
        print(key,val)


async def test_all_suppliers():
    result = await supplier_name_index()
    assert isinstance(result, list) 
    #print("All Suppliers:", result)


#run(test_all_suppliers())