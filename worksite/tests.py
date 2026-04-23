from asyncio import run
from os import listdir

#from apps.SiteProject.project import ( create_project, read_project, delete_project, get_workers , get_worker, all_projects, get_account)
from core.baseModels.project_models import Project
from core.utilities.utils import json_file_writer, join_words, space_words, check_create_filepath
#from apps.SiteProject.analytics import IncomeDataFrame
#from apps.SiteWorker.worker import ( all_workers, get_worker, all_workers_data )

#from bs4 import BeautifulSoup

from core.baseModels.rate_models import IndustryRateModel
from apps.SiteRate.rate import all_rates
from apps.SiteSupplier.supplier import (all_suppliers)#, get_supplier, get_supplier_by_name, save_supplier, delete_supplier ,all_suppliers_ref, supplier_name_index )
from config import BASE_PATH

project_ids:list = ['DD13673', 'JR42706', 'KS03093', 'LM8603' ]


async def test_all_projects():
    result =await all_projects()
    assert isinstance(result, list) 
    print("All Projects:", result)
    
    
async def test_read_project( id:str=project_ids[0] ):
    project =await read_project(id=id)
    assert isinstance(project, Project) 
    project.load_account()
    project.load_dayswork()
    project.load_jobs()
    #print(f"Project {id}:", project)
    return project
    

def test_get_account():
    
    result = get_account(project_id="KS03093") # type: ignore
    assert result is not None
    print( result)

#test_all_projects()
#test_get_account()

async def test_all_workers():
    result = await all_workers_data()
    assert isinstance(result, list) 
    js_data = dict()
    for item in result:
        del item['value']['_rev']
        js_data[item['id']] = item['value']
        
    
    #print("All Workers:", js_data) 
    return js_data 


async def test_get_worker():
    result = await get_worker(id="AG37282") # type: ignore
    assert result is not None
    #print( result.address)
    for item in result.address:
        key, val = item
        print(key,val)


async def test_all_rates():
    result = await all_rates()
    assert isinstance(result, list) 
    js_data = dict()
    for item in result:
        rate:IndustryRateModel = IndustryRateModel()
        rate.load_data(item)
        js_data[rate.id] = rate.model_dump()
        
    
    print("All Rates:", js_data) 
    
    return js_data 


async def test_all_suppliers():
    result = await all_suppliers()
    assert isinstance(result, list) 
    js_data = dict()
    for item in result:
        del item['value']['_rev']
        js_data[item['id']] = item['value']
        
    
    #print("All Workers:", js_data) 
    return js_data 
    
    




async def test_file_writer():
    from pathlib import Path
    file_location = Path(__file__).parent.parent.parent
    directory = file_location / 'jsonDB'
    project =await test_all_suppliers() 
    file_path=directory / f"suppliers.json"
    #print(file_path)
    result = json_file_writer(file_path=file_path, data=project ) 
    print(result)

#run(test_all_suppliers())
#run(test_file_writer()) #test_all_suppliers())



'''html = """<table border="0" cellpadding="0" cellspacing="0" class="month">
<tr><th colspan="7" class="month">November 2025</th></tr>
<tr><th class="mon">Mon</th><th class="tue">Tue</th><th class="wed">Wed</th><th class="thu">Thu</th><th class="fri">Fri</th><th class="sat">Sat</th><th class="sun">Sun</th></tr>
<tr><td class="noday">&nbsp;</td><td class="noday">&nbsp;</td><td class="noday">&nbsp;</td><td class="noday">&nbsp;</td><td class="noday">&nbsp;</td><td class="sat">1</td><td class="sun">2</td></tr>
<tr><td class="mon">3</td><td class="tue">4</td><td class="wed">5</td><td class="thu">6</td><td class="fri">7</td><td class="sat">8</td><td class="sun">9</td></tr>
<tr><td class="mon">10</td><td class="tue">11</td><td class="wed">12</td><td class="thu">13</td><td class="fri">14</td><td class="sat">15</td><td class="sun">16</td></tr>
<tr><td class="mon">17</td><td class="tue">18</td><td class="wed">19</td><td class="thu">20</td><td class="fri">21</td><td class="sat">22</td><td class="sun">23</td></tr>
<tr><td class="mon">24</td><td class="tue">25</td><td class="wed">26</td><td class="thu">27</td><td class="fri">28</td><td class="sat">29</td><td class="sun">30</td></tr>
</table>
"""
active_days=['8','12','16','24']


def plot_month_higlight_dates(html, dates:list=[]):
    soup = BeautifulSoup(html, 'html.parser')
    # style the table
    table = soup.find('table')
    table.attrs['class'].append('bg-base-50 text-xs shadow-sm')

    # style the active days
    tds = soup.find_all('td')    
    td = tds[12]    
    for td in tds:
        if td.text in active_days:
            td.attrs['class'].append('bg-blue-500')
            #print('active', td)

    return(soup)

month = plot_month_higlight_dates(html, active_days)
print(month)'''
