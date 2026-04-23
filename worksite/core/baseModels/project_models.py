from typing import ( Any, )

from pydantic import ( BaseModel, Field )
from core.utilities.utils import ( generate_id, timestamp, ) 
from core.baseModels import ( AccountTransactions, Bank, DayPay, InvoiceModel, SupplierInvoiceRecord, WithdrawalModel, PaybillModel,
    PayItem, Payment, PayStatement )
from core.baseModels import ( Contact, ReportModel )
from core.baseModels import ( Address, AddressLocation )
from core.baseModels.employee_models import (DayWorkModel, WorkerTask, ProjectWorker)
from core.baseModels.jobtask_models import ( JobModel, JobTask )
from core.baseModels.rate_models import ( IndustryRateModel )
from core.baseModels.eventstate_models import ( Event, State, ComonActionModel )
from core.baseModels.measurments_models import ( EstimateModel )
from core.baseModels.data_models import ( MetaData, )
from core.baseModels.auth_models import ( User, )


from database.mongo_dms import ( async_client, client )

# Setup
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



# Project Activity Logs

class ActivityLog(BaseModel):
    id:int = Field(default=timestamp()) 
    title:str = Field(default='') 
    description:str = Field(default='')  

    def load_data(self, data:dict={} ):
        if data:
            
            if data.get('id'):
                self.id = data.get('id', 0)

            if data.get('title'):
                self.id = data.get('title', '')

            if data.get('description'):
                self.id = data.get('description', '')
        else:
            pass



class ProjectAccountRecords(BaseModel):
    invoices:list[InvoiceModel] = []
    purchase_orders:list[Any] = []
    salary_statements:list[PayStatement] = []
    paybills:list[PaybillModel] = []


    def load_data(self, data:dict={} ):
        if data:
            if data.get('invoices'):
                for item in data.get('invoices', []):
                    invoice:InvoiceModel = InvoiceModel()
                    invoice.load_data(data=item)
                    self.invoices.append(invoice)
            if data.get('purchase_orders'):
                self.purchase_orders = data.get('purchase_orders', [])

            if data.get('salary_statements'):
                for item in data.get('salary_statements', []):
                    statement:PayStatement = PayStatement()
                    statement.load_data(data=item)
                    self.salary_statements.append(statement)
            if data.get('paybills'):
                for bill in data.get('paybills', []):
                    paybill:PaybillModel = PaybillModel()
                    paybill.load_data(data=bill)
                    self.paybills.append(paybill)  
            else:
                pass
        else:
            pass

    # Manage Invoices 
    @property
    def invoice_report(self)->dict:
        return {
            'count': len(self.invoices),
            'total_purchases': float( sum( [ invoice.total for invoice in self.invoices ] )),
            'total_tax': float( sum( [ invoice.tax for invoice in self.invoices ] ))
        }
    
    @property
    def invoice_numbers(self)->list:
        return  [ invoice.invoiceno for invoice in self.invoices ] 
    
    @property
    def bill_ids(self):
        return [ bill.id for bill in self.paybills ]
    

    def invoice_ids_index(self)->list:
        return [ invoice.id for invoice in self.invoices ]


    def record_invoice(self, invoice:InvoiceModel):
        '''Records a loaded invoice model '''
        if invoice.invoiceno in self.invoice_numbers: # Check exists
            pass
        else:
            self.invoices.append(invoice)


    def add_invoice(self, form_data:dict={} ):
        '''creates a new invoice model and return a SupplierInvoiceRecord Model'''
        
        new_invoice:InvoiceModel = InvoiceModel()
        record:SupplierInvoiceRecord = SupplierInvoiceRecord()
        statement:WithdrawalModel = WithdrawalModel()
        if form_data: # Check for data
            if form_data.get('invoiceno') in self.invoice_numbers: # Check exists
                pass
            else:                        
                if form_data.get('supplier'): 
                    new_invoice.supplier.load_data(data=form_data.get('supplier', {}))
                if form_data.get('invoiceno'):
                    new_invoice.invoiceno = form_data.get('invoiceno', '')
                if form_data.get('date'):
                    new_invoice.date = timestamp(form_data.get('date', ''))
                if form_data.get('items'):
                    for item in form_data.get('items', []):
                        new_invoice.add_item(item)              
                if form_data.get('tax'):
                    new_invoice.tax = float(form_data.get('tax', 0))
                if form_data.get('total'):
                    new_invoice.total = float(form_data.get('total', 0))
                if form_data.get('billed'):
                    new_invoice.billed = form_data.get('billed', False)
                
                self.invoices.append(new_invoice)
                ## Update suppliers record                
                record.inv_id = new_invoice.id
                record.invoiceno = new_invoice.invoiceno
                record.date = new_invoice.date
                record.total = new_invoice.total
                ## prepare withdrawal statement                
                statement.date = new_invoice.date
                statement.ref = f'{new_invoice.id}-{new_invoice.invoiceno}'
                statement.amount = new_invoice.total
                statement.recipient.name = new_invoice.supplier.name
                return { 
                    "supplier_invoice_record": record,
                    "withdrawal_statement": statement 
                }
                # update project withdrawals
        else:
            return { 
                    "supplier_invoice_record": record,
                    "withdrawal_statement": statement  
                }
        


    def get_paybill(self, bill_id:str='')->PaybillModel:
        if bill_id in self.bill_ids:
            bill:PaybillModel = [ bill for bill in self.paybills if bill.id == bill_id ][0]
            return bill
        return PaybillModel()
    
    
    # Manage Pay Statements
    @property
    def statement_ids(self)->list['str']:
        return [ statement.id for statement in self.salary_statements ]
    
    ## Add Pay Statement
    def add_pay_statement(self, pay_statement:PayStatement):
        if pay_statement.id in self.statement_ids:
            pass
        else:
            self.salary_statements.append(pay_statement)

    ## Get Pay Statement
    def get_pay_statement(self, pay_statement_id:str=''):
        if pay_statement_id in self.statement_ids:
            return  [statement for statement in self.salary_statements if statement.id == pay_statement_id ][0]
        return 
        

    ## Remove Pay Statement
    def remove_pay_statement(self, pay_statement_id:str=''):
        if pay_statement_id in self.statement_ids:
            pay_statement:PayStatement = self.get_pay_statement(pay_statement_id=pay_statement_id) # type: ignore
            self.salary_statements.remove(pay_statement) #ignore type           
        else:
            pass



class ProjectExpenceModel(BaseModel):
    id:str = Field(default=generate_id(name='account expence') )
    ref:str = Field(default="")
    date:int = timestamp()
    description:str = Field(default="")
    claimant:str = Field(default="")
    total:float = Field(default= 0.001)
    method:str = Field(default="cash")    
    user:str = Field(default="sytem")

    def load_data(self, data:dict={})->None:
        if data:
            if data.get('id'):
                self.id = data.get('id', '')
            if data.get('ref'):
                self.ref = data.get('ref', '')
            if data.get('date'):
                self.date = timestamp(data.get('date', ''))
            if data.get('description'):
                self.description = data.get('description', '')
            if data.get('claimant'):
                self.claimant = data.get('claimant', '')
            if data.get('total'):
                self.total = float(data.get('total', ''))
            if data.get('method'):
                self.method = data.get('method', '')
            
            if data.get('user'):
                self.user = data.get('user', '')
            
        else:
            pass



class ProjectExpences(BaseModel):
    expences:list[ProjectExpenceModel] = []
    total:float = Field(default=0.0) 

    def load_data(self, data:list=[])->None:
        if data and type(data) == list:
            for item in data:
                expence = ProjectExpenceModel()
                expence.load_data(item)

                self.expences.append(expence)
            self.calculate_total
        else:
            pass

    @property
    def calculate_total(self):
        if self.expences:
            self.total = float( sum( [ expence.total for expence in self.expences ] ) )



class ProjectAccount(BaseModel):
    bank:Bank = Bank()
    budget:float = Field(default=0.0)
    ballance:float = Field(default=0.0)
    started:int = Field( default=0 ) # timestamp
    updated:int = Field( default=0 )
    transactions:AccountTransactions = AccountTransactions()
    expences:ProjectExpences = ProjectExpences()
    records:ProjectAccountRecords = ProjectAccountRecords()

    
    def load_data(self, data:dict={} ):
        if data:
            if data.get('bank'):
                self.bank.load_data(data=data.get('bank', {}))
            if data.get('budget'):
                self.budget = float(data.get('budget', 0.0))
            if data.get('ballance'):
                self.ballance = float(data.get('ballance', 0.0))
            if data.get('started'):
                self.started = int(data.get('started', 0.0))
            if data.get('updated'):
                self.updated = int(data.get('updated', 0.0))
            if data.get('transactions'):
                self.transactions.load_data(data=data.get('transactions', []))
            if data.get('expences'):
                self.expences.load_data(data= data.get('expences', []))
                self.expences.calculate_total
            if data.get('records'):
                self.records.load_data( data=data.get('records', {}) )
        
            
        else:
            pass

    
    def update_budget(self, resource:str='', data:float= 0.0) -> None:
        if resource and data:
            if resource == 'budget':
                self.budget = data
                self.updated = timestamp()

    
    def get_paybill(self, id:str=''):
        ''''''
        bill = [ bill for bill in self.records.paybills if bill.id == id ] # type: ignore
        if bill:
            return bill[0]
        return {}



class ProjectClient(BaseModel):
    name:str = Field(default='')
    contact:Contact  = Contact()
    address:Address = Address()

    def load_data(self, data:dict={}):
        if data:
            # assignments
            if data.get('name'):
                self.name = data.get('name', '')

            self.contact.load_data(data=data.get('contact', {}))
            
            self.address.load_data(data=data.get('address', {}))
            
        else:
            pass



class ProjectStaff(BaseModel):
    accountant:str = Field(default='')
    architect:str = Field(default='')
    engineer:str = Field(default='')
    quantitysurveyor:str = Field(default='')
    landsurveyor:str = Field(default='')
    supervisors:list[str] = []

    def load_data(self, data:dict={} ):
        if data:
            if data.get('accountant'):
                self.accountant = data.get('accountant', '')
            if data.get('architect'):
                 self.architect = data.get('architect', '')
            if data.get('engineer'):
                self.engineer = data.get('engineer', '')
            if data.get('quantitysurveyor'):
                self.quantitysurveyor = data.get('quantitysurveyor', '')
            if data.get('landsurveyor'):
                self.landsurveyor = data.get('landsurveyor', '')
            if data.get('supervisors'):
                for item in data.get('supervisors', []):
                    if item not in self.supervisors:
                        self.supervisors.append(item)
            
        else:
            pass



class ProjectAdmin(BaseModel):
    leader:str = Field(default='')
    staff:ProjectStaff = ProjectStaff()

    def load_data(self, data:dict={} ):
        if data:
            if data.get('loader'):
                self.leader = data.get('leader', '')
            if data.get('staff'):
                self.staff.load_data( data=data.get('staff', {}) )
           
        else:
            pass



class ProjectProgress(BaseModel):
    overall:float = Field( default=0.0)
    planning:float = Field( default=0.0)
    design:float = Field( default=0.0)
    estimates:float = Field( default=0.0)
    contract:float = Field( default=0.0)
    development:float = Field( default=0.0)
    build:float = Field( default=0.0)
    unit:str = Field( default='%')

    def load_data(self, data:dict={} ):
        if data:

            if data.get('overall'):
                self.overall = data.get('overall', 0.0)

            if data.get('planning'):
                self.planning = data.get('planning', 0.0)

            if data.get('design'):
                self.design = data.get('design', 0.0)
            if data.get('estimates'):
                self.estimates = data.get('estimates', 0.0)
            if data.get('contract'):
                self.contract = data.get('contract', 0.0)
            if data.get('development'):
                self.development = data.get('development', 0.0)
            if data.get('build'):
                self.build = data.get('build', 0.0)
            if data.get('unit'):
                self.unit = data.get('unit', 0.0)
            
        else:
            pass




class Project(BaseModel):
    id:str = Field(default='')
    name:str = Field(default='')    
    category:str = Field(default='')
    standard:str = Field(default='')
    address:AddressLocation = Field(default = AddressLocation())
    owner:ProjectClient = ProjectClient() 
    account:ProjectAccount = ProjectAccount()
    admin:ProjectAdmin = ProjectAdmin()
    workers:list[ProjectWorker] = []
    jobs:list[JobModel] = []
    rates:list[IndustryRateModel] = []
    days:list[DayWorkModel] = []
    inventories:dict = {}
    action:ComonActionModel = ComonActionModel()
    event:Event = Event()
    state:State = State()
    progress:ProjectProgress = ProjectProgress()
    activity_logs:list[ActivityLog] = []
    reports:list[ReportModel] = []
    estimates:list[EstimateModel] = []
    metadata:MetaData = MetaData()
    model_config = {
        "extra": "allow" 
    }


    @property
    def _id(self)->str:
        return self.id

    @property
    def create_id(self):
        if self.name:
            self.id = generate_id(name=self.name)
        else:
            self.id = generate_id(name=self.name)

    @property
    def project(self):
        project:dict = self.model_dump()
        project['_id'] = self.id
        try:
            return project
        finally:
            del project

    @property
    def update_build_progress(self):
        jobs_progress:list = [int(job.progress) for job in self.jobs ]
        if len(jobs_progress) > 0:
            self.progress.build = int((sum(jobs_progress) / len(jobs_progress)))
        else:
            pass


    def update(self, revision:str)->dict:
        project:dict = self.project
        project['_rev'] = revision
        try:
            return project
        finally:
            del project


    @property
    def unload_extensions(self)->None:
        '''Removes all extensions from the model
         call before saving or updating the data.'''
        
        try:
            if hasattr(self, 'industry_rates'):
                del self.industry_rates # pyright: ignore[reportAttributeAccessIssue]
        except (AttributeError, ValueError):
            pass
        

    ## Workers Index
    @property
    def workers_index(self)->list:
        """The Projects Workers ID index

        Returns:
            list: List of workers Id 
        """
        return [ worker.key for worker in self.workers ]
    

    ## Job Id Index
    @property
    def job_index(self)->list:
        """The Projects Job ID index

        Returns:
            list: List of Job Id 
        """
        return [ job.id for job in self.jobs ]
    
    ## Job Title Index
    @property
    def job_title_index(self)->list:
        """The Projects Job titles index

        Returns:
            list: List of Job titles 
        """
        return [ job.title for job in self.jobs ]
    

    ## Task Index
    @property
    def task_index(self)->list:
        """The Projects Tasks ID index

        Returns:
            list: List of Task Id 
        """
        task_ids:list = []
        for job in self.jobs:
            task_ids.extend(job.task_ids)

        return task_ids

    @property
    def project_labour_cost(self)->dict:
        '''The total cost of labour for the project'''
        project_cost = {
            'total': 0.0,
            'tasks': 0.0,
            'contractor': 0.0,
            'misc': 0.0,
            'insurance': 0.0,
            'overhead': 0.0
        }
        for job in self.jobs:
            job.recalculate
            project_cost['total'] += job.cost.total.metric
            project_cost['tasks'] += job.cost.task
            project_cost['contractor'] += job.cost.contractor
            project_cost['misc'] += job.cost.misc
            project_cost['insurance'] += job.cost.insurance
            project_cost['overhead'] += job.cost.overhead

        return project_cost
    
    # Load Project Workers
    def load_workers(self, data:dict={}):
        if data:
            _data:dict = data
        else:
            _data = workers_collection.find_one({"_id": self.id}) # type: ignore

        if _data.get('workers'):
            for item in _data.get('workers', []):
                worker:ProjectWorker = ProjectWorker()
                worker.load_data(data=item)
                worker.tasks = [task for task in worker.tasks if task.project == self.id ]
                worker.jobs = set([task.job_id for task in worker.tasks if task.project == self.id ]) # type: ignore
                self.workers.append(worker)
            # debug worker
        else:
            pass
    

    def load_jobs(self, data:dict={}):
        if data:
            pass
        else:
            data = job_collection.find_one({"_id": self.id}) # type: ignore

        if data.get('jobs'):
            for item in data.get('jobs', []):
                job:JobModel = JobModel()
                job.load_data(data=item)
                self.jobs.append(job)
            self.update_build_progress
        else:
            pass
    


    def load_rates(self, data:dict={}):
        if data:
            pass
        else:
            data = rate_collection.find_one({"_id": self.id}) # pyright: ignore[reportAssignmentType]

        if data.get('rates'):
            for item in data.get('rates', []):
                rate:IndustryRateModel = IndustryRateModel()
                rate.load_data(data=item)
                self.rates.append(rate)
        else:
            pass


    def load_dayswork(self, data:dict={}):
        if data:
            pass
        else:
            data = daywork_collection.find_one({"_id": self.id}) # type: ignore
        if data.get('days'):
            for item in data.get('days', []):
                day:DayWorkModel = DayWorkModel()
                day.load_data(data=item)
                self.days.append(day)
        else:
            pass


    def load_inventories(self, data:dict={}):
        if data:
            pass
        else:
            data = inventory_collection.find_one({"_id": self.id}) # type: ignore
        if data.get('inventorys'):            
                self.inventories = data.get('inventorys', {})
        if data.get('inventories'):            
                self.inventories = data.get('inventories', {})
        else:
            pass


    def load_account(self, data:dict={}):
        if data:
            pass
        else:
            data = account_collection.find_one({"_id": self.id}) # type: ignore
        if data.get('account'):
            self.account.load_data(data=data.get('account', {}))
        else:
            pass


    def load_logs(self, data:dict={}):
        if data:
            pass
        else:
            data = logs_collection.find_one({"_id": self.id}) # type: ignore
        if data.get('activity_logs'):
            for item in data.get('activity_logs', []):
                log_item:ActivityLog = ActivityLog()
                log_item.load_data( data=item )
                self.activity_logs.append( log_item )
                # debug alog
        else:
            pass


    def load_reports(self, data:dict={}):
        if data:
            pass
        else:
            data = report_collection.find_one({"_id": self.id}) # type: ignore
        if data.get('reports'):
            for item in data.get('reports', []):
                report:ReportModel = ReportModel()
                report.load_data(data=item)
                self.reports.append(report)
        else:
            pass


    def load_estimates(self, data:dict={}):
        if data:
            pass
        else:
            data = estimate_collection.find_one({"_id": self.id}) # type: ignore
        if data.get('estimates'):
            for item in data.get('estimates', []):
                estimate:EstimateModel = EstimateModel()
                estimate.load_data(data=item)
                self.estimates.append(estimate)
        else:
            pass


    def load_data(self, data:dict={}):
        if data.get('id'):
            self.id = data.get('id', '')
        elif data.get('_id'):
            self.id = data.get('_id', '')
        if data.get('name'):
            self.name = data.get('name', '')
        if data.get('category'):
            self.category = data.get('category', '')
        if data.get('standard'):
            self.standard = data.get('standard', '')                
        self.address.load_data(data=data.get('address', {}))
        self.owner.load_data(data=data.get('owner', {}))        
        self.admin.load_data(data=data.get('admin', {}))
        self.action.load_data(data=data.get('action', {}))
        self.event.load_data(data=data.get('event', {}))
        self.state.load_data(data=data.get('state', {}))
        self.progress.load_data(data=data.get('progress', {}))
        if data.get('metadata', {}):
            self.metadata.load_data(data=data.get('metadata', {}))
        elif data.get('meta_data', {}):
            self.metadata.load_data(data=data.get('meta_data', {}))
       

      
    def load_new_form_data(self, form_data:dict={}, user:User=User() )->None:
        if form_data:         
            self.name = form_data.get('name', '')
            self.category = form_data.get('category', '')
            self.standard = form_data.get('standard', '')
            self.address.load_data({
                            "lot": form_data.get('lot'), 
                            "street": form_data.get('street'), 
                            "town": form_data.get('town'),
                            "city_parish": form_data.get('city_parish'),
                            "country": form_data.get('country', "Jamaica") 
                        })
            self.owner.name = form_data.get('owner', '')
            self.admin.leader = form_data.get('lead', '') 

            self.metadata.created = timestamp(date=form_data.get('date', ''))
            self.metadata.created_by = user.username  

            self.create_id
            
            self.log_activity(title='Created', description=f"This Project was  created by User {user.username}")
            
        else:
            pass

    # Load External Data
    ## Load Industry Rates
    def load_industry_rates(self, rates_list:list=[]):
        self.industry_rates = rates_list
                  
    # Accounting    
    def update_budget(self, figure:float=0.0)->None:
        #jobs_costs = [float(job.cost.total.metric) for job in self.jobs ]
        ''' Adds the figure to the project budget '''
        self.account.budget = self.account.budget + float( figure )
    
    
    # Worker and job crew management
    def add_worker(self, data:dict={})->list[ProjectWorker]:
        '''Add a worker to the project's workers index'''
        if data.get("_id") in self.workers_index:
            pass
        else:
            worker:ProjectWorker = ProjectWorker()
            worker.load_data(data=data)
            if worker:
                worker.assigned = timestamp()
                self.workers.append(worker)
                self.log_activity(
                title='Worker Addition', 
                description=f"Worker with Id {worker.id} was added to the project's workers index"
            )
        return self.workers 
    
    
    ## Get worker
    def get_worker(self, worker_id:str='')->ProjectWorker:
        '''Retreive a worker from the project's workers index'''
        return [ worker for worker in self.workers if worker.id == worker_id ][0]

    
    ## Remove worker
    def remove_worker(self, worker_id:str='')->list[ProjectWorker]:
        '''Removes a worker from the project's workers index'''
        worker = self.get_worker(worker_id=worker_id)
        if worker:
            self.workers.remove(worker)
        return self.workers
    
    ## Assign worker to task
    def assign_worker_task(self, worker_id:str='', job_id:str='', task_id:str='')->None:
        '''Assigns a worker to a task'''
        job:JobModel = self.get_job(job_id=job_id)
        worker_task:WorkerTask = job.assign_worker_task(worker_id=worker_id, task_id=task_id)
        worker_task.project = self.id
        worker:ProjectWorker = self.get_worker(worker_id=worker_id)
        worker.add_task(task = worker_task)

    ## Unassign worker from task
    def unassign_task_worker(self, worker_id:str='', job_id:str='', task_id:str='')->None:
        '''Unassigns a worker from a task'''
        job:JobModel = self.get_job(job_id=job_id)
        job.unassign_worker_task(worker_id=worker_id, task_id=task_id)
        worker:ProjectWorker = self.get_worker(worker_id=worker_id)
        worker.remove_task(task_id=task_id)

    # Job Crew Management
    ## Add crew member to job
    def add_job_crew(self, worker_id:str='', job_id:str='')->list[ProjectWorker]:
        '''Returns an updated list of crew members '''
        job:JobModel = self.get_job(job_id=job_id)
        worker:ProjectWorker = self.get_worker(worker_id=worker_id)
        if job and worker:
            return job.crew.add_crew_member(worker=worker)
        return job.crew.memebrs
        
    ## Get crew member from job
    def get_job_crew(self, worker_id:str='', job_id:str='')->ProjectWorker:
        '''Returns a single crew member '''
        job:JobModel = self.get_job(job_id=job_id)
        return job.crew.get_crew_member(worker_id=worker_id)
    
    ## Remove crew member from job  
    def remove_job_crew(self, worker_id:str='', job_id:str='')->list[ProjectWorker]:
        '''Returns an updated list of crew members '''
        job:JobModel = self.get_job(job_id=job_id)
        return job.crew.remove_crew_member(worker_id=worker_id)
        
    
    # Job Management
     ## Add Jobs
    def add_job(self, job:JobModel=JobModel(), user:User=User())->list[JobModel]:
        '''Creates a new Job instance from data'''
        if job.id in self.job_index or job.title in self.job_title_index : ### check if job exist already
            pass
        else:
            job.project_id = self.id  ### assign the project's id
            self.jobs.append(job) ### add job
            self.log_activity(title='New Job Created', description=f'A new job with id {job.id} was created by {user.username}') ### log activity
        return self.jobs

       
    ## Get Job
    def get_job(self,job_id:str='')->JobModel: # type: ignore
        if job_id:
            if job_id in self.job_index:
                job:JobModel = [job for job in self.jobs if job.id == job_id][0]
                return job
            
        else:
            return JobModel()
        
    ## Get Jobs
    @property
    def jobs_data(self)->list[JobModel]: # type: ignore
        return [ job.model_dump() for job in self.jobs ] # type: ignore

    ## Update Job
    def update_job(self, job_id:str='', form_data:dict={} )->list[JobModel]:
        job:JobModel = self.get_job( job_id=job_id )
        if job.title:
            job.load_form_data(form_data=form_data)
        else:
            pass
        return self.jobs
    
    
    ## Delete Job
    def delete_job(self, job_id:str='' )->list[JobModel]:
        '''Removes the requested job from the projects Jobs 
        and return the project jobs 
        '''
        job:JobModel = self.get_job( job_id=job_id )
        if job.title:
            self.jobs.remove(job) 
            self.log_activity( 
            title='Job Deletion', 
            description=f'Job with id {job_id} was removed from The Project.' 
            )           
        else:
            pass
        return self.jobs
    
    
    # Rate Management
    def save_rate(self, rate:IndustryRateModel=IndustryRateModel())->list[IndustryRateModel]:
        '''Saves a new industry rate to the project rates index'''
        if rate.title in [ r.title for r in self.rates ]:
            pass
        elif rate.description in [ r.description for r in self.rates ]:
            pass
        else:
            rate.id = f'{self.id}-{rate.id}'
            self.rates.append(rate)
            self.log_activity(title='New Rate Added', description=f'Industry Rate with id {rate.id} was added to the project rates index')
        return self.rates
        


    ## Get industry rate .
    def get_industry_rate(self, rate_id:str=''):
        '''Retrieves a rate object from the industry rates index '''
        if rate_id:
            return [rate for rate in self.industry_rates if rate.id == rate_id ][0] # pyright: ignore[reportAttributeAccessIssue]
        
    ## Get project rate .
    def get_rate(self, rate_id:str=''):
        '''Retrieves a rate object from the project's rates index '''
        if rate_id:
            return [rate for rate in self.rates if rate.id == rate_id ][0]
        
    # Task Management
    ## Assign task
    def assign_task(self, job_id:str='', task_id:str='')->None:
        '''Converts an industry rate to a Job Task and 
        assigns it to a job
        '''        
        try:
            job = self.get_job(job_id=job_id)
            task = self.get_rate(rate_id=task_id)
           
            if job and task:               
                job_task:JobTask = JobTask(
                    id = f"{job.id}-{task_id.split('-')[1]}",
                    title = task.title,
                    description= task.description,
                    metric=task.metric,
                    imperial= task.imperial, 
                    category=task.category
                )
                job.add_task(task=job_task)
                self.log_activity(title='Job Task Assignment', description=f'Task with id {task.id} was added to Job {job.id} ')

        except Exception as ex:
            print(str(ex))


    ## Retreive a task
    def get_task(self, job_id:str='', task_id:str='')->JobTask:
        job:JobModel = self.get_job(job_id=job_id)
        return job.get_task(task_id=task_id)
    

    ## Update task
    def update_task(self, job_id:str='', task_id:str='', resource:str='', form_data:dict={})->JobModel:
        '''Updates a task's properties bassed on resource request
        '''  
        job = self.get_job(job_id=job_id)
        task = job.get_task(task_id=task_id)      
        try:
            if job and task: 
                task.update_resource(resource=resource, form_data=form_data)
                job.recalculate
                self.log_activity(
                    title='Task Property Update', 
                    description=f'Task with id {task_id} of Job with id {job_id} {resource} property was updated'
                )
            return job

        finally:
            del job
            del task                


    ## Delete task
    def delete_task(self,  job_id:str='', task_id:str='')->JobModel:
        job:JobModel = self.get_job(job_id=job_id)
        job.delete_task(task_id=task_id)
        job.recalculate
        self.log_activity( 
            title='Task Deleted', 
            description=f'Task with id {task_id} was removed from Job with id {job_id}.' 
            )
        try:

            return job
        finally:
            del job

    # Event State Management
    def update_state(self, state:str, date:str | None = None):
        self.state.set_state(state=state)
        self.event.update_event(event=state, event_date=date)
        self.log_activity(title="Project State Update", description=f"The project state was updated to {state}.")
        
    # Activity Logs Management
    def log_activity(self, title:str='', description:str='')->None:

        log = ActivityLog( title=title, description=description ) 
        try:
            self.activity_logs.append(log)
        finally:
            del(log) 

         

    @property
    def project_phases(self)->dict:
        """Construction development phases

        Returns:
            dict: key value of project phases
        """        
        return {     
                    
                'preliminary':'Preliminary',
                'substructure': 'Substructrue',
                'superstructure': 'Superstructure',
                'floors': 'Floors',
                'roofing': 'Roofing',
                'installations': 'Installations',
                'electrical': 'Electrical',
                'plumbung': 'Plumbing',
                'finishes': 'Finishes',
                'landscaping': 'Landscaping',      
                
        }
    


def project_phases()->dict:
    """Construction development phases

    Returns:
        dict: key value of project phases
    """        
    return {     
                    
                'preliminary':'Preliminary',
                'substructure': 'Substructrue',
                'superstructure': 'Superstructure',
                'floors': 'Floors',
                'roofing': 'Roofing',
                'installations': 'Installations',
                'electrical': 'Electrical',
                'plumbung': 'Plumbing',
                'finishes': 'Finishes',
                'landscaping': 'Landscaping',      
                
        }