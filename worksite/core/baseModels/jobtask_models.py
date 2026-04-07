from typing import ( Any, )
from http import HTTPStatus
from pydantic import ( BaseModel, Field,  AliasChoices )
from core.utilities.utils import ( generate_id, timestamp, convert_price_by_unit, convert_unit)
from core.baseModels.measurments_models import ( MetricModel, ImperialModel, Output )
from core.baseModels.eventstate_models import ( Event, State )
from core.baseModels.data_models import ( MetaData, )
from core.baseModels.employee_models import (DayWorkModel, WorkerPersonalModel, WorkerTask) 
from core.baseModels.employee_models import ( ProjectWorker, )



class JobPayment(BaseModel):
    id:str = Field(default=generate_id(name='Job Payment', sec=6))
    amount:float = Field(default= 0.0) # Amount to be paid out
    deduction:float = Field(default= 0.0) # Amount to be paid out
    date:int = Field(default = timestamp()) # The payment date
    percent:int = Field(default= 0) # The percent value of the job progress
    total:float = Field(default= 0.0) 

    def load_data(self, data:dict={}):
        if data:
            if data.get('amount'):
                self.amount = float(data.get('amount', 0.0))
            if data.get('deduction'):
                self.deduction = float(data.get('deduction', 0.0))
            if data.get('date'):
                self.date = timestamp(date=data.get('date', ''))
            if data.get('percent'):
                self.percent = int(data.get('percent', 0))           
            self.calculate_total
        else:
            pass 
        
    @property
    def calculate_total(self)->None:
        self.total = self.amount - self.deduction



class JobTotal(BaseModel):
    imperial:float = Field(default=0.0)
    metric:float = Field(default=0.0)
    fees:float = Field(default=0.0)


class JobFees(BaseModel):
    contractor:int = Field(default=0)
    insurance:int = Field(default=0)
    misc:int = Field(default=0)
    overhead:int = Field(default=0)
    unit:str = Field(default="%")
    
    def load_data(self, data:dict={}):
        if data:
            if data.get('contractor'):
                self.contractor = data.get('contractor', 0)
            if data.get('insurance'):
                self.insurance = data.get('insurance', 0)
            if data.get('misc'):
                self.misc = data.get('misc', 0)
            if data.get('overhead'):
                self.overhead = data.get('overhead', 0)
                
        else:
            pass


class JobCost(BaseModel):
    task:float = Field(default=0.0)
    contractor:float = Field(default=0.0)
    misc:float = Field(default=0.0)
    insurance:float = Field(default=0.0)
    overhead:float = Field(default=0.0)
    total:JobTotal = JobTotal()
    unit:str = Field(default="$")
 
    def load_data(self, data:dict={}):
        if data:
            if data.get('task'):
                self.task = data.get('task', 0)
            if data.get('contractor'):
                self.contractor = data.get('contractor', 0)
            if data.get('insurance'):
                self.insurance = data.get('insurance', 0)
            if data.get('misc'):
                self.misc = data.get('misc', 0)
            if data.get('overhead'):
                self.overhead = data.get('overhead', 0)
            
        else:
            pass


class JobPaymentResult(BaseModel):
    paid:bool = Field(default=False) 
    payments:list[JobPayment] = []
    
    def load_data(self, data:dict={}):
        if data:
            if data.get('paid'):
                self.paid = data.get('paid', False) 
            if data.get('payments'):
                self.payments = data.get('payments', []) 
            
        else:
            pass


class JobCrew(BaseModel):
    name:str = Field(default='')
    rating:int = Field(default=0)
    members:list[ProjectWorker] = []   
    state:State = State()
    
    def load_data(self, data:dict={}):
        if data:
            if data.get('name'):
                self.name = data.get('name', '')
            if data.get('rating'):
                self.rating = int(data.get('rating', 0))
            if data.get('members'):
                for member_data in data.get('members', []):
                    crew_member:ProjectWorker = ProjectWorker()
                    crew_member.load_data(data=member_data)

                    self.members.append(crew_member)

            self.state.load_data( data.get('state', {}) )
                
        else:
            pass
  

    @property
    def members_index(self):
        return [ worker.id for worker in self.members ]  


    # Add crew memeber
    def add_crew_member(self, worker:ProjectWorker=ProjectWorker())->list[ProjectWorker]:
        '''Add a member to the job crew'''

        if worker.id in self.members_index:
            pass
        else:
            self.members.append(worker)
        return self.members
        
        
    def get_crew_member(self, worker_id:str='')->ProjectWorker:
        '''Retreive a member from the job crew'''
        return [ worker for worker in self.members if worker.id == worker_id ][0]

    
    def remove_crew_member(self, worker_id:str='')->list[ProjectWorker]:
        '''Removes a worker from the job crew'''
        worker = self.get_crew_member(worker_id=worker_id)
        if worker:
            self.members.remove(worker)
        return self.members
    

class JobTask(BaseModel):
    id:str = Field(default='', validation_alias=AliasChoices('id', '_id'))  
    title:str = Field(default='')
    description:str = Field(default='')
    metric: MetricModel = MetricModel()
    imperial: ImperialModel = ImperialModel()
    state:State = State()
    event:Event = Event()
    assigned:bool =Field(default=False)
    assignedto:list[str] = []
    phase:str = Field(default='')
    paid:JobPaymentResult = JobPaymentResult()

    #timestamp:int = Field(default=0) # depricated
    progress:int = Field(default=0)
    output:Output = Output()
    category:str = Field(default='')
    metadata: MetaData = MetaData()

      
    def load_data(self,  data:dict={} )->None:
        """
        Loads an existing task dict into a JobTask Model
        
        :param flag: An optional flag string informs either that a task is new in which case
        a unique resource id (UID) is generated or to return a property of the task
        :type flag: str
        :param data: A dictionary containing the task's data to be loaded into the model
        :type data: dict
        :return: A JobTask model with data
        :rtype: JobTask
        
            Note: Acccepted flags.  new, id , title, etc... 
        """    
        if data:        
            #process id property
            if data.get('_id'):    # Data Availability Check DA
                self.id = data.get('_id', '')  # Assignment
            elif data.get('id'):
                self.id = data.get('id', '')
            
            #process title property
            if data.get('title'):    
                self.title = data.get('title', '')
            
            #process description property
            if data.get('description'):
                self.description = data.get('description', '')

            #process metric property   
            self.metric.load_data(data=data.get('metric', {}))    
           

            # process imperial property
            self.imperial.load_data(data=data.get('imperial', {}))  

            self.state.load_data(data=data.get('state', {}))
            self.event.load_data(data=data.get('event', {}))
            
            if data.get('assigned'):
                self.assigned = data.get('assigned', False)
            if data.get('assignedto'):
                if type(data.get('assignedto')) == str :
                    self.assignedto.append(data.get('assignedto', '')) # if string update
                else:
                    self.assignedto = data.get('assignedto', '') # if list assign            
                
            #process job phase property
            if data.get('phase'): # Data Availability Check DAC
                self.phase = data.get('phase', '') # Assignment
                
            #process paid property
            self.paid.load_data(data=data.get('paid', {}))
                
            #process progress property   
            if data.get('progress'):
                self.progress = int(data.get('progress', 0)) 
            
                # process task output properties
            self.output.load_data(data=data.get('output', {}))

            #process category property    
            if data.get('category'):
                self.category = data.get('category', '') 
            
            # process task metadata properties
            if data.get('meta_data'):
                self.metadata.load_data(data=data.get('meta_data', {})) 
            elif data.get('metadata'):
                self.metadata.load_data(data=data.get('metadata', {})) 
            #process timestamp property    
            if data.get('timestamp'):
                if self.metadata.created > 1: # if a created timestamp is present ignore 
                    pass
                else:
                    self.metadata.created = data.get('timestamp', 0.0) # else update with timestamp
        else:
            pass
    
    
    def update_resource(self, resource:str='', form_data:dict={}):
        if resource and form_data:
            if resource == 'property':
                if form_data.get('title'):
                    self.title = form_data.get('title', '')
                if form_data.get('description'):
                    self.description = form_data.get('description', '')
                if form_data.get('category'):
                    self.category = form_data.get('category', '')
                if form_data.get('phase'):
                    self.phase = form_data.get('phase', '')                
                if form_data.get('assignedto'):
                    self.assignedto.append(form_data.get('assignedto', ''))
                    self.assigned = True

                if form_data.get('progress'):
                    self.progress = int(form_data.get('progress', 0))
                ## Process Metric updates
            if resource == 'metric':
                if form_data.get('munit'):
                    self.metric.unit = form_data.get('munit', '')
                if form_data.get('mprice'):
                    self.metric.price = round( float(form_data.get('mprice', 0.0)), 2)

                    unit_price:dict = convert_price_by_unit( unit=form_data.get('munit', ''), value=float( form_data.get('mprice', 0.0)) )

                    self.imperial.unit = unit_price.get('unit', '')
                    self.imperial.price = round( unit_price.get('value', 0.0), 2 )
                        

                if form_data.get('mquantity'):
                    self.metric.quantity = round( float(form_data.get('mquantity', 0.0)), 3 )
                    unit_quantity:dict = convert_unit( unit=form_data.get('munit', ''), value=float( form_data.get('mquantity', 0.0)) )
                    
                    self.imperial.quantity = round( unit_quantity.get('value', 0.0), 3)

                if form_data.get('moutput'):
                    self.output.metric = float(form_data.get('moutput', ''))
                    self.metric.calculate_total
                    self.imperial.calculate_total
            ## Process Imperial updates
            if resource == 'imperial':
                if form_data.get('unit'):
                    self.imperial.unit = form_data.get('unit', '')
                if form_data.get('price'):
                    self.imperial.price = round( float(form_data.get('price', 0.00)), 2 )

                    unit_price:dict = convert_price_by_unit( unit=form_data.get('unit', ''), value=float( form_data.get('price', 0.0)) )

                    self.metric.unit = unit_price.get('unit', '')
                    self.metric.price = round( unit_price.get('value', 0.0), 2 )

                if form_data.get('quantity'):
                    self.imperial.quantity = round( float(form_data.get('quantity', 0.0)), 3)
                    unit_quantity:dict = convert_unit( unit=form_data.get('unit', ''), value=float( form_data.get('quantity', 0.0)) )
                
                    self.metric.quantity = round( unit_quantity.get('value', 0.0), 3 )

                if form_data.get('output'):
                    self.output.imperial = float(form_data.get('output', ''))
                self.imperial.calculate_total
                self.metric.calculate_total

            if resource == 'revenue':                
                payment:JobPayment = JobPayment(
                    amount= float(form_data.get('payamount', 0.0)),
                    deduction=float(form_data.get('deduction', 0.0))
                )
                payment.calculate_total
                if form_data.get('payment_date'):
                    payment.date = timestamp(form_data.get('payment_date', ''))
                payment.percent = self.progress
                self.paid.payments.append(payment)
                if payment.percent == 100:
                    self.paid.paid = True

            if resource == 'state':
                pass
            if resource == 'event':
                pass


        else:
            pass
        return self
        

   
class JobModel(BaseModel):
    id: str = Field(default='', validation_alias=AliasChoices('id', '_id'))
    project_id: str = Field(default='')
    title: str = Field(default='')
    description:str = Field(default='')
    projectPhase: str = Field(default='')
    crew:JobCrew = JobCrew()
    worker:str = Field(default='')
    tasks:list[JobTask] = []
    event:Event = Event()
    state:State = State()
    fees:JobFees = JobFees()
    cost:JobCost = JobCost()
    progress:int = Field(default=0)
    result:JobPaymentResult = JobPaymentResult()
    
    @property
    def generate_job_id(self)->None:
        '''
        Generate a unique resource identifier "UID" for
        the JobModel
        
        :param self: Requires the title of the JobModel "self.title",
        will resort to the JobModel description "self.description" or a default value is generated if none is present. 
        
        :Note : The head of the "UID" refferences the title or description of the Job. Enshure that either present before executing this function. 
        '''
        if self.title:
            self.id = generate_id(name=self.title)
        else:
            self.id = generate_id(name=self.description)
        return
    ## Task Index
    
    @property
    def task_ids(self)->list:
        return [task.id for task in self.tasks]    

    
    @property
    def update_progress(self):
        tasks_progress:list = [int(task.progress) for task in self.tasks ]
        if len(tasks_progress) > 0:
            self.progress = int((sum(tasks_progress) / len(tasks_progress)))



    def load_data(self, data:dict={}):
        '''Loads existing data into the Model'''
        if data:
            # assignments
            if data.get('id'):
                self.id = data.get('id', '')
            elif data.get('_id'):
                self.id = data.get('_id', '')
            if data.get('project_id'):
                self.project_id=data.get('project_id', '') 
            if data.get('title'):
                self.title=data.get('title', '')
            if data.get('description'):
                self.description=data.get('description', '')
            if data.get('projectPhase'):
                self.projectPhase=data.get('projectPhase', '')
            if data.get('worker'):
                self.worker = data.get('worker', '')
            if data.get('progress'):
                self.progress = data.get('progress', '')
            # loads
            self.crew.load_data(data=data.get('crew', {}))
            
            self.event.load_data( data=data.get('event', {}) )   
            
            self.state.load_data( data=data.get('state', {}) )
            self.fees.load_data( data=data.get('fees', {}) )
            self.cost.load_data(data=data.get('cost', {}))
            self.result.load_data(data=data.get('result', {}))
            
            # load Tasks
            if data.get('tasks', []):
                for item in data.get('tasks', []):  
                    task:JobTask = JobTask()
                    task.load_data(data=item)  
                    self.add_task(task=task) 
                    #sleep(0.001) 
            else:
                pass 
            self.update_progress
            self.recalculate
                
        else:
            pass

    
    def load_new_form_data(self, form_data:dict={} )->None:
        if form_data: 
            if form_data.get('title'):
                self.title = form_data.get('title', '')
            if form_data.get('description'):
                self.description = form_data.get('description', '')
            if form_data.get('projectPhase'):
                self.projectPhase = form_data.get('projectPhase', '')
            if form_data.get('crew_name'):
                self.crew.name = form_data.get('crew_name', '')
            if form_data.get('date'):
                self.event.created = timestamp(date=form_data.get('date', ''))
            # load fees    
            if form_data.get('fees_contractor'):
                self.fees.contractor = int(form_data.get('fees_contractor', ''))
            if form_data.get('fees_insurance'):
                self.fees.insurance = int(form_data.get('fees_insurance', ''))
            if form_data.get('fees_misc'):
                self.fees.misc = int(form_data.get('fees_misc', ''))
            if form_data.get('fees_overhead'):
                self.fees.overhead = int(form_data.get('fees_overhead', ''))
            self.generate_job_id        
            
        else:
            pass
        

    def load_form_data(self, form_data:dict={} )->None:
        if form_data: 
            if form_data.get('title'):
                self.title = form_data.get('title', '')
            if form_data.get('description'):
                self.description = form_data.get('description', '')
            if form_data.get('projectPhase'):
                self.projectPhase = form_data.get('projectPhase', '')
            if form_data.get('crew_name'):
                self.crew.name = form_data.get('crew_name', '')
            if form_data.get('date'):
                self.event.created = timestamp(date=form_data.get('date', ''))
            # load fees    
            if form_data.get('fees_contractor'):
                self.fees.contractor = int(form_data.get('fees_contractor', ''))
            if form_data.get('fees_insurance'):
                self.fees.insurance = int(form_data.get('fees_insurance', ''))
            if form_data.get('fees_misc'):
                self.fees.misc = int(form_data.get('fees_misc', ''))
            if form_data.get('fees_overhead'):
                self.fees.overhead = int(form_data.get('fees_overhead', ''))
                   
            
        else:
            pass
        


    def add_task(self, task:JobTask)->HTTPStatus:        
        if task:
            if task.id in self.task_ids:
               return HTTPStatus(409)
            else:
                self.tasks.append(task)
                self.update_progress
                self.recalculate
                return HTTPStatus(200)
    
    
    def get_task(self, task_id:str='')->JobTask:        
        task:JobTask = [task for task in self.tasks if task.id == task_id][0]
        try:
            return task
        finally:
            del task

    
    def delete_task(self, task_id:str='')->None:        
        task:JobTask = [task for task in self.tasks if task.id == task_id][0]
        try:
            self.tasks.remove(task)
        finally:
            self.update_progress
            self.recalculate
            del task

    
    def assign_worker_task(self, worker_id:str='', task_id:str='')->WorkerTask:
        '''Assigns task to a worker '''
        worker:ProjectWorker = self.crew.get_crew_member(worker_id=worker_id)
        task:WorkerTask = WorkerTask()
        if worker.id:
            task.job_id=self.id
            task.id=task_id
            task.assignment_date=timestamp()
            
        
            if task.id not in [item.id for item in worker.tasks]:
                worker.tasks.append(task )

        return task
            

    def unassign_worker_task(self, worker_id:str='', task_id:str='')->None:
        '''Unassigns a task from a worker'''
        worker:ProjectWorker = self.crew.get_crew_member(worker_id=worker_id)
        task = [item for item in worker.tasks if item.id == task_id][0]
        if task:
            worker.tasks.remove(task )
    
       
    def add_event(self, event:dict={})->None:
        self.event.load_data(data=event)               
            
    def add_state(self, state:dict={})->None:
        self.state.load_data(data=state) 
        
    def add_fees(self, fees:dict={})->None:
        self.fees.load_data(data=fees)

    def add_cost(self, cost:dict={})->None:
        self.cost.load_data(data=cost)

    
    @property
    def recalculate(self)->None:
        metric_costs:list = [float(task.metric.total) for task in self.tasks ]
        total_costs:float = sum(metric_costs)
        imperial_costs:list = [float(task.imperial.total) for task in self.tasks ]

        self.cost.task = total_costs
        self.cost.contractor = float(self.fees.contractor / 100) * total_costs
        self.cost.misc = float(self.fees.misc / 100) * total_costs
        self.cost.insurance = float(self.fees.insurance / 100) * total_costs
        self.cost.overhead = float(self.fees.overhead / 100) * total_costs
        fees:list = [self.cost.contractor, self.cost.misc, self.cost.insurance, self.cost.overhead]
        totals:list = [total_costs, sum(fees)]
        self.cost.total.metric = sum(totals)
        self.cost.total.imperial = sum(imperial_costs)
        self.cost.total.fees = sum(fees)
        return 

 