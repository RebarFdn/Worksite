 ## Application Data Models

## vscode-fold=0

from enum import Enum

from pydantic import BaseModel, Field, AliasChoices
from core.utilities.utils import generate_id, timestamp

#from models.supplier_models import Supplier


class UserRoles(str, Enum):
    ADMIN = 'ADMIN'
    GUEST = 'GUEST'
    USER = 'USER'
    STAFF = 'STAFF'
    WORKER = 'WORKER'
    

class Department(str, Enum):
    HR = 'HR'
    SALES = 'SALES'
    IT = 'IT'
    ENGINEERING = 'ENGINEERING'
    CONSTRUCTION= 'CONSTRUCTION'


class Role(str, Enum):    
    STAFF = 'STAFF'
    WORKER = 'WORKER'
    TEMPORARY = 'TEMPORARY'


# Data 

class Database(BaseModel):
    name:str = Field(default='')
    partitioned:bool = Field(default=False)
    
    def load_data(self, data:dict={}):
        if data:
            if data.get('name'):
                self.name = data.get('name', '')
            if data.get('partitioned'):
                self.partitioned = data.get('partitioned', False)
        else:
            pass



class MetaData(BaseModel):
    created: int = Field(default=0)
    updated: int = Field(default=0)
    database:Database = Database()
    created_by:str = Field(default='')
    model_config = {
        "extra": "allow" 
    }
    
    def load_data(self, data:dict={}):
        if data:
            if data.get('created'):
                if type(data.get('created') == int):
                    self.created = data.get('created', 0)
                else:
                    self.created = timestamp(date= data.get('created',''))
            if data.get('created_by'):
                self.created_by = data.get('created_by', '')
            if data.get('database'):
                db:Database = Database()
                db.load_data(data=data)
                self.database = db
            if data.get('cloned'):
                self.cloned =  data.get('cloned')
            if data.get('updated'):
                self.updated = data.get('updated', 0)
        else:
            pass



class SupplierStub(BaseModel):
    id: str = Field(default='', validation_alias=AliasChoices('id', '_id'))
    name:str = Field(default='')     
    taxid: str = Field(default='')

    def load_data(self, data:dict={})->None:
        if data:
            if data.get('id'):
                self.id = data.get('id', '')
            if data.get('name'):
                self.name = data.get('name', '')
            if data.get('taxid'):
                self.taxid = data.get('taxid', '')
        else:
            pass
    


class InventoryItem(BaseModel):   
    ref:str = Field(default= '') 
    name:str = Field(default= '') 
    amt:int = Field(default= 0) 
    unit:str = Field(default= '') 
    stocking_date:int = Field(default=timestamp()) 
    supplier:SupplierStub = SupplierStub()

    def load_data(self, data:dict={}):
        if data:
            if data.get('item'):
                self.item = data.get('item')
            if data.get('item'):
                self.item = data.get('item')
            if data.get('item'):
                self.item = data.get('item')
            if data.get('item'):
                self.item = data.get('item')
            if data.get('item'):
                self.item = data.get('item')
            if data.get('item'):
                self.item = data.get('item')
        else:
            pass 
    

class Inventory(BaseModel): 
    id:str = Field(default=generate_id(name='Material Inventory', sec=8))
    name:str = Field(default='')
    items:list[InventoryItem] = []
    dispenced:list = []

    def load_data(self, data:dict={}):
        if data:
            for key, value in data.items():
                if key =='id':
                    if value:
                        self.id = value
                if key =='name':
                    if value:
                        self.name = str(value)
                if key =='items':
                    #TODO sort, assign and append
                    if value:
                        self.items = value
                if key =='dispenced':
                    #TODO sort, assign and append
                    self.dispenced = value
        else:
            pass
    
    @property
    def stocking(self)->list:        
        return [item.amt for item in self.items ]
    
    @property
    def stock(self):        
        return sum(self.stocking)
    
    @property
    def stock_usage(self)->int:           
        store = 0
        if len(self.dispenced) > 0:
            for item in self.dispenced:
                store += item[1]                
        else: pass
        return store
    
    @property
    def available_stock(self):       
        return self.stock - self.stock_usage


# A standard project Template        
def project_template(key:str=''):
    """A standard Project Template 
    representing a the most common elements of a 
    construction project.

    Args:
        key (str, optional): an element of the construction project. Defaults to None.
    
    Usage:
        >>> project_template('address')
        --- {'lot': None, 'street': None, ...}
    """
    PROJECT_TEMPLATE = dict( 
                name = "Test Project",
                category = "residential",
                standard = "metric",
                address = {"lot": None, "street": None, "town": None,"city_parish": None,"country": "Jamaica","coords": {
                "lat": 0,
                "lon": 0
                } },
                owner = {
                "name": None,
                "contact": {},
                "address": {"lot": None, "street": None, "town": None,"city_parish": None,"country": None, }
            },
                account = {
                    "bank": {
                        "name": None,
                        "branch": None,
                        "account": None,
                        "account_type": None
                        },
                    "budget": None,
                    "ballance": 0,
                    "started": timestamp(),
                    "transactions": {
                        "deposit": [], 
                        "withdraw": []
                    },
                    "expences": [],
                    "records": {
                        "invoices": [],
                        "purchase_orders": [],
                        "salary_statements": [],
                        "paybills": []
                    }
                },
                admin = {
                "leader": None,
                "staff": {
                "accountant": None,
                "architect": None,
                "engineer":None,
                "quantitysurveyor": None,
                "landsurveyor": None,
                "supervisors": []
                }
    },
                workers = [],
                jobs = [],
                rates = [],
                days = [],
                inventorys = [],            
                event = {
                    "started": 0,
                    "completed": 0,
                    "paused": [],
                    "restart": [],
                    "terminated": 0
                },
                state =  {
                    "active": False,
                    "completed": False,
                    "paused": False,
                    "terminated": False
                },      
                progress =  {
                "overall": None,
                "planning": None,
                "design": None,
                "estimates": None,
                "contract": None,
                "development": None,
                "build": None,
                "unit": None
                },
                activity_logs = [],
                reports = [],
                estimates = [],
                meta_data = None
                
                )
    if key: return PROJECT_TEMPLATE.get(key)
    else: return PROJECT_TEMPLATE
