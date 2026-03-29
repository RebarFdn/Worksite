from typing import ( List, Any )
from pydantic import ( BaseModel, EmailStr, Field )
from pydantic_extra_types.phone_numbers import ( PhoneNumber, )
from modules.utils import ( generate_id, timestamp )
from models.addresslocation_models import ( Address, )
from models.comunication_modules import ( Contact, ReportModel )
from models.accounting_models import ( Bank,DayPay,  Loan, Payment, PayStatement )
from models.data_models import ( MetaData, )


class DayWorkModel(BaseModel):
    id:str = Field(default='')
    project_id:str = Field(default='')   
    worker_name:str = Field(default='')
    date:int = Field(default=0)
    start:str = Field(default='')
    end:str = Field(default='')
    description:str = Field(default='')
    payment:DayPay = DayPay()
    hash_key:bytes = Field(default=b'')

    def load_data(self, data:dict={} ):
        if data:
            if data.get('id'):
                self.id = data.get('id', '')

            if data.get('project_id'):
                self.project_id = data.get('project_id', '')

            if data.get('worker_name'):
                self.worker_name = data.get('worker_name', '')
            
            if data.get('date'):
                if type( data.get('date') == str ):
                    self.date = timestamp( date=data.get('date', ''))
                else:
                    self.date = data.get('date', 0 )

            if data.get('start'):
                self.start = data.get('start', '')

            if data.get('end'):
                self.end = data.get('end', '')
            
            if data.get('description'):
                self.description = data.get('description', '')
            
            if data.get('hash_key'):
                self.hash_key = data.get('hash_key', '')

            self.payment.load_data(data=data.get('payment', ''))
        else:
            pass
      

# Information
class Identity(BaseModel):
    identity: str = Field(default= '')
    id_type: str = Field(default= '')
    trn: str = Field(default= '')
    
    def load_data(self, data:dict={}):
        if data:
            if data.get('identity'):
                self.identity = data.get('identity', '')
            if data.get('id_type'):
                self.id_type = data.get('id_type', '')
            if data.get('trn'):
                self.trn = data.get('trn', '')
        else:
            pass


class Occupation(BaseModel):
    occupation: str = Field( default='' )
    rating: int = Field( default=0 ) 
    
    def load_data(self, data:dict={}):
        if data:
            if data.get('occupation'):
                self.occupation = data.get('occupation', '')
            if data.get('rating'):
                self.rating = int(data.get('rating', ''))
            
        else:
            pass
 
 

class NextOfKin(BaseModel):
    name: str = Field(default='')
    relation: str =  Field(default='')
    address: Address = Address()
    contact: Contact = Contact()

    def load_data(self, data:dict={}):
        if data:
            if data.get('name'):
                self.name = data.get('name', '')
            if data.get('relation'):
                self.relation = data.get('relation', '')
            if data.get('address'):
                self.address.load_data(data=data.get('address', {}))
            if data.get('contact'):
                self.contact.load_data(data=data.get('contact', {}))
        else:
            pass
    

class EmployeeState(BaseModel):
    employed: bool = Field(default=False)    
    on_leave: bool = Field(default=False)
    terminated: bool = Field(default=False)
    active: bool = Field(default=False) 
    
    def load_data(self, data:dict={}):
        if data and type(data) == dict:            
            if data.get('on_leave'):
                self.on_leave = data.get('on_leave', False)                
            if data.get('terminated'):
                self.terminated = data.get('terminated', False)
            if data.get('active'):
                self.active = data.get('active', False)
                if self.active:
                    self.employed = True
        else:
            pass 
      

class EmployeeEvent(BaseModel):
    employed: int = Field(default=timestamp())
    started: int = Field(default=timestamp())
    on_leave: List[ int ] = []
    resumption: List[ int ] = []
    terminated: int = Field(default=timestamp())

    def load_data(self, data:dict={}):
        if data and type(data) == dict:
            if data.get('employed'):
                self.employed = timestamp(date=data.get('employed', ''))
            if data.get('started'):
                self.started = timestamp(date=data.get('started', ''))
            if data.get('on_leave'):
                self.on_leave = data.get('on_leave',[])
            if data.get('resumption'):
                self.resumption = data.get('resumption', [])
            if data.get('terminated'):
                self.terminated = timestamp(date = data.get('terminated', ''))
        else:
            pass 
    

class EmployeeStats(BaseModel):
    sex: str =  Field(default='')
    dob: int = Field(default=timestamp())
    height: str =  Field(default='')
    
    def load_data(self, data:dict={}):
        if data:
            if data.get('sex'):
                self.sex = data.get('sex' ,'')
            if data.get('dob'):
                self.dob = timestamp(date=data.get('dob', ''))
            if data.get('height'):
                self.height = data.get('height', '')
        else:
            pass 
    


class EmployeeJobTasks(BaseModel):
    jobs: List[ Any ] = []
    tasks: List[ Any ] = []
        
    def load_data(self, data:dict={}):
        if data:
            if data.get('jobs'):
                self.jobs = data.get('jobs', [])
            if data.get('tasks'):
                self.tasks = data.get('tasks', [])
        else:
            pass 
    


class EmployeeAccount(BaseModel):
    bank:Bank = Bank()
    payments: List[PayStatement] = []
    loans: List[Loan] = []
    
    def load_data(self, data:dict={}):
        if data:
            if data.get('bank'):
                self.bank.load_data(data= data.get('bank', {}))
            if data.get('payments'):
                for item in data.get('payments', []):
                    payment:PayStatement = PayStatement()
                    payment.load_data(data=item)
                    self.payments.append(payment)
            if data.get('loans'):
                self.loans = data.get('loans', [])
        else:
            pass 
    
    
    @property
    def payment_ref_index(self)->list[str]:
        if self.payments:
            return [payment.bill_ref for payment in self.payments]
        return []
    
    def get_pay_statement(self, project_id:str='', bill_ref:str=''):
        pay_statement = [ statement for statement in self.payments if statement.bill_ref == bill_ref and statement.project == project_id ]    
        if pay_statement:
            return pay_statement[0]
        return 
    
    def save_pay_statement(self, pay_statement:PayStatement):
        
        if pay_statement.bill_ref in self.payment_ref_index:
            pass
        else:
            
            self.payments.append(pay_statement)
        return pay_statement
    
    def remove_pay_statement(self, bill_ref):
        if bill_ref in self.payment_ref_index:
            payment:PayStatement = self.get_pay_statement(bill_ref=bill_ref)
            self.payments.remove(payment)
        return self.payments


        

class EmployeeModel(BaseModel):

    id:str = Field(default= '')
    name: str = Field(default= '')
    oc: str = Field(default= '')
    sex: str = Field(default= '')
    dob: int = Field(default= 0)
    identity: str = Field(default= '')
    id_type: str = Field(default= '')
    trn: str = Field(default= '')     
    occupation: str = Field(default= '')    
    rating: int = Field(default= 0)   
    height: str = Field(default= '') 
    imgurl: str = Field(default= '')    
    address: Address  = Address()
    contact: Contact = Contact()
    account: EmployeeAccount = EmployeeAccount()
    nok: NextOfKin = NextOfKin()
    tasks: list[str] = []  
    jobs: list[str] = [] 
    days: list[DayWorkModel] = [] 
    state: EmployeeState  = EmployeeState()
    event: EmployeeEvent  = EmployeeEvent()    
    role: str = Field(default='WORKER') 
    reports:list[ ReportModel ] = []
    health_issues: list[str] = []
    metadata: MetaData = MetaData()
    rev:str = Field(default='')

    @property
    def generate_id(self):
        if self.name:
            self.id = generate_id( name=self.name )
        else:
            self.id = generate_id( name='Company Employee' )

    @property
    def _id(self)->str:
        return self.id

    
    @property
    def employee(self):
        worker = self.model_dump()
        worker["_id"] = self.id
        #worker["_rev"] = self.rev
        #del worker['rev']
       
        return worker
    

    def load_data(self, data:dict={}):
        if data:
            if data.get('id'):
                self.id = data.get('id', '')
            else:
                self.id = data.get('_id', '')
            if data.get('name'):
                self.name = data.get('name', '')
            if data.get('oc'):
                self.oc = data.get('oc', '')
            if data.get('identity'):
                self.identity = data.get('identity', {})
            if data.get('id_type'):
                self.id_type = data.get('id_type', '')
            if data.get('trn'):
                self.trn = data.get('trn', '')                
            if data.get('sex'):
                self.sex = data.get('sex' ,'')
            if data.get('dob'):
                self.dob = timestamp(date=data.get('dob', ''))
            if data.get('height'):
                self.height = data.get('height', '')        
            if data.get('occupation'):
                self.occupation = data.get('occupation', {})
            if data.get('rating'):
                self.rating = data.get('rating',0)            
            
            if data.get('imgurl'):
                self.imgurl = data.get('imgurl', '')
            if data.get('address'):
                self.address.load_data(data= data.get('address', {}))
            if data.get('contact'):
                self.contact.load_data(data = data.get('contact', {}))
            if data.get('account'):
                self.account.load_data(data = data.get('account', {}))
            if data.get('nok'):
                self.nok.load_data(data = data.get('nok', {}))
            if data.get('tasks'):
                self.tasks = data.get('tasks', [])
            if data.get('jobs'):
                self.jobs = data.get('jobs', [])
            if data.get('state'):
                self.state.load_data(data = data.get('state', {}))
            if data.get('event'):
                self.event.load_data(data = data.get('event', {}))            
            if data.get('role'):
                self.role = data.get('role', '')
            if data.get('reports'):
                for report in data.get('reports', []):
                    report_model = ReportModel()
                    report_model.load_data(data=report)
                    self.reports.append( report_model )
            if data.get('health_issues'):
                self.health_issues = data.get('health_issues', [])
            if data.get('metadata'):
                self.metadata.load_data(data= data.get('metadata', {}))
            if data.get('_rev'):
                self.rev =  data.get('_rev')
               
        else:
            pass 
    
    
            
    def load_new_form_data(self, form_data:dict={}, user:str='' )->None:
        if form_data: 
            if form_data.get('name'):         
                self.name = form_data.get('name', '')
            if form_data.get('oc'):         
                self.oc = form_data.get('oc', '')
            if form_data.get('sex'):         
                self.sex = form_data.get('sex', '')
            if form_data.get('dob'):         
                self.dob = form_data.get('dob', '')
            if form_data.get('height'):         
                self.height = form_data.get('height', '')
            if form_data.get('identity'):         
                self.identity = form_data.get('identity', '')
            if form_data.get('id_type'):         
                self.id_type = form_data.get('id_type', '')
            if form_data.get('trn'):         
                self.trn = form_data.get('trn', '')
            if form_data.get('occupation'):         
                self.occupation = form_data.get('occupation', '')
            if form_data.get('rating'):         
                self.rating = int(form_data.get('rating', ''))
            
            if form_data.get('lot'):         
                self.address.lot = form_data.get('lot', '')
            if form_data.get('street'):         
                self.address.street = form_data.get('street', '')
            if form_data.get('town'):         
                self.address.town = form_data.get('town', '')
            if form_data.get('city_parish'):         
                self.address.city_parish = form_data.get('city_parish', '')
            if form_data.get('country'):         
                self.address.country = form_data.get('country', '')
            if form_data.get('tel'):         
                self.contact.tel = form_data.get('tel', '')
            if form_data.get('mobile'):         
                self.contact.mobile = form_data.get('mobile', '')
            if form_data.get('watsapp'):         
                self.contact.watsapp = form_data.get('watsapp', '')
            if form_data.get('email'):         
                self.contact.email = form_data.get('email', '')
            if form_data.get('bank_name'):         
                self.account.bank.name = form_data.get('bank_name', '')
            if form_data.get('branch'):         
                self.account.bank.branch = form_data.get('branch', '')
            if form_data.get('account_type'):         
                self.account.bank.account_type = form_data.get('account_type', '')
            if form_data.get('account'):         
                self.account.bank.account = form_data.get('account', '')
            if form_data.get('kin_name'):         
                self.nok.name = form_data.get('kin_name', '')
            if form_data.get('kin_relation'):         
                self.nok.relation = form_data.get('kin_relation', '')
            if form_data.get('kin_tel'):         
                self.nok.contact.tel = form_data.get('kin_tel', '')
            
            self.generate_id
            self.imgurl = f"/static/imgs/workers/{self.id}.png"
            self.metadata.created_by = user
            self.metadata.created = timestamp()
            self.metadata.database.name = 'site-workers'
                    
        else:
            pass


    def add_job(self, job_id:str=''):
        if job_id and job_id not in self.jobs:
            self.jobs.append(job_id)
    
    def add_task(self, task_id:str=''):
        if task_id and task_id not in self.tasks:
            self.tasks.append(task_id)


class WorkerPersonalModel(BaseModel):
    name:str = Field(default='')
    oc:str = Field(default='')
    occupation:str = Field(default='')
    rating:int = Field(default=0)
    imgurl:str = Field(default='static/imgs/workers/.png')
    email: EmailStr = Field(default='')
    mobile: PhoneNumber | None = None

    def load_data(self, data:dict={} ):
        if data:
            for key, value in data.items():
                if key == 'name':
                    if value:
                        self.name = str(value)
                if key == 'oc':
                    if value:
                        self.oc = str(value)
                if key == 'occupation':
                    if value:
                        self.occupation = str(value)
                if key == 'rating':
                    if value:
                        self.rating = int(value)
                if key == 'imgurl':
                    if value:
                        self.imgurl = str(value)
                if key == 'email':
                    if value:
                        self.email = str(value)
                if key == 'mobile':
                    if value:
                        self.mobile = value            
        else:
            pass


class WorkerTask(BaseModel):
    job_id:str = Field(default='')    
    id:str = Field(default='')
    assignment_date:int = Field(default=timestamp())
    model_config = {
        "extra": "allow" 
    }

    def load_data(self, data:dict={} ):
        if data:
            for key, value in data.items():
                if key == 'project':
                    if value:
                        self.project = str(value)
                if key == 'job_id':
                    if value:
                        self.job_id = str(value)
                if key == 'id':
                    if value:
                        self.id = str(value)
                if key == 'assignment_date':
                    if value:
                        if type(value) == str:
                            self.assignment_date = timestamp(date=value)
                        else:
                            self.assignment_date = int(value)
        else:
            pass

