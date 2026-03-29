from typing import ( Any, )
from http import HTTPStatus
from pydantic import ( BaseModel, Field,  AliasChoices )
from core.utilities.utils import ( generate_id, timestamp, )
from core.baseModels.measurments_models import ( MetricModel, ImperialModel, Output )
from core.baseModels.data_models import ( MetaData, )



# Jobs and Tasks
class IndustryRateModel(BaseModel):
    id: str = Field(default='', validation_alias=AliasChoices('id', '_id'))  
    title: str = Field(default='')
    description: str = Field(default='')
    category:str=Field(default='')
    metric: MetricModel = MetricModel()
    imperial: ImperialModel = ImperialModel()
    output: Output = Output()        
    comments: list[Any] = []        
    metadata: MetaData = Field(default=MetaData(), validation_alias=AliasChoices('meta_data', 'metadata'))
    
    ## Generate Id
    @property
    def generate_id(self)->None:
        '''
        Generate a unique resource identifier "UID" for
        the IndustryRateModel
        
        :param self: Requires the title of the IndustryRateModel "self.title",
        will resort to the IndustryRateModel description "self.description" or a default value is generated if none is present. 
        
        :Note : The head of the "UID" refferences the title or description of the IndustryRateModel. Enshure that either present before executing this function. 
        '''
        if self.title:
            self.id = generate_id(name=self.title)
        else:
            self.id = generate_id(name=self.description)
        return

    @property
    def rate(self)->dict:
        '''Returns the IndustryRateModel data as a dict with the id property as _id for database compatibility.
        '''
        out_rate:dict = self.model_dump()
        out_rate['_id'] = self.id
        try:
            return out_rate
        finally:
            del out_rate


    ## Load rate data into model 
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
                
            #process category property    
            if data.get('category'):
                self.category = data.get('category', '')           
                
            #process metric property   
            self.metric.load_data(data=data.get('metric', {}))    
            #print(self.metric) # debug
            
            # process imperial property
            self.imperial.load_data(data=data.get('imperial', {}))  
            
                # process task output properties
            self.output.load_data(data=data.get('output', {}))
            
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


    ## Create new rate from form data
    def load_form_data(self, form_data:dict={} )->None:
        if form_data: 
            if form_data.get('title'):
                self.title = form_data.get('title', '')
            if form_data.get('description'):
                self.description = form_data.get('description', '')
            if form_data.get('category'):
                self.category = form_data.get('category', '')
            if form_data.get('date'):
                self.metadata.created = timestamp()
            if form_data.get('metric_unit'):
                self.metric.unit = form_data.get('metric_unit', '')
            if form_data.get('metric_price'):
                self.metric.price = round( float(form_data.get('metric_price', 0.0)), 2 )
            if form_data.get('metric_output'):
                self.output.metric = float(form_data.get('metric_output', 0.0))
            if form_data.get('imperial_unit'):
                self.imperial.unit = form_data.get('imperial_unit', '')
            if form_data.get('imperial_price'):
                self.imperial.price = round( float(form_data.get('imperial_price', 0.0)), 2 )
            if form_data.get('imperial_output'):
                self.output.imperial = float(form_data.get('imperial_output', 0.0))
            ## Gerenate Id for new rate 
            if self.id == '':
                self.generate_id
        else:
            pass
        
        return
    
    ## Set Cloned status
    def set_cloned(self, cloned_from:str='')->None:
        status:bool=False
        if cloned_from:
            status = True
        self.metadata.cloned = {
            "from": cloned_from,
            "status": status
            }
        
