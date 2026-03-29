from typing import List, Any

from pydantic import BaseModel, EmailStr, Field,  SecretStr, AliasChoices, ValidationError
from pydantic_extra_types.country import CountryShortName 
from pydantic_extra_types.phone_numbers import PhoneNumber

try:
    from modules.utils import generate_id, timestamp, datimestamp, convert_timestamp, tally, convert_price_by_unit,convert_unit
except ImportError:
    from utils import generate_id, timestamp, datimestamp, convert_timestamp, tally, convert_price_by_unit,convert_unit


# Measured Quantity Models
# Metric
class MetricModel(BaseModel):
    unit:str = Field(default='')
    price:float = Field(default=0.001)
    quantity:float = Field(default=0.001)
    total:float = Field(default=0.001)
    
    def load_data(self, data:dict={}):
        """
        Load Metric data from a dictionary
                
        :param self: Description
        :param data: Description
        :type data: dict
        """
        if data.get('unit'): # check
            self.unit = data.get('unit', '') # assignment
        if data.get('price'):
            self.price = float( data.get('price', 0.001))
        if data.get('quantity'):
            self.quantity = float( data.get('quantity', 0.001))
        self.calculate_total        
    
    @property
    def calculate_total(self):
        self.total = self.price * self.quantity


class ImperialModel(BaseModel):
    unit:str = Field(default='')
    price:float = Field(default=0.001)
    quantity:float = Field(default=0.001)
    total:float = Field(default=0.001)
    
    def load_data(self, data:dict={}):
        """
        Load Imperial data from a dictionary
        
        :param self: Description
        :param data: Description
        :type data: dict
        """
        if data.get('unit'):
            self.unit = data.get('unit', '')
        if data.get('price'):
            self.price = float( data.get('price', 0.001))
        if data.get('quantity'):
            self.quantity = float( data.get('quantity', 0.001))
        self.calculate_total        
    
    @property
    def calculate_total(self):
        self.total = self.price * self.quantity


class Output(BaseModel):
    metric:float = 0.001
    imperial:float = 0.001
    
    def load_data(self, data:dict={}):
        if data:
            if data.get('metric'): # Check
                self.metric = data.get('metric', 0.001)
            if data.get('imperial'):
                self.imperial = data.get('imperial', 0.001)    
        else:
            pass


class EstimateItem(BaseModel):
    no:int = Field( default=0)
    title:str = Field( default='')
    description:str = Field(default='')
    metric:MetricModel = MetricModel()
    imperial:ImperialModel = ImperialModel()
    
    def load_data(self, data:dict={} ):
        if data:
            if data.get('no'):
                self.no = data.get('no', '')
            if data.get('title'):
                self.id = data.get('title', '')
            if data.get('description'):
                self.id = data.get('description', '')
            self.metric.load_data(data=data.get('metric', {}))
            self.imperial.load_data(data=data.get('imperial', {}))
        else:
            pass


class EstimateModel(BaseModel):
    id:str = Field(default='') 
    author:str = Field(default='')
    date:int = Field(default=timestamp())
    title:str = Field(default='') 
    description:str = Field(default='')
    itemlist:list[EstimateItem] = []  

    def load_data(self, data:dict={} ):
        if data.get('id'):
            self.id = data.get('id', '')
        if data.get('author'):
            self.author = data.get('author', '')
        if data.get('date'):
            self.date = data.get('date', '')
        if data.get('date'):
            self.date = data.get('date', '')
        if data.get('title'):
            self.id = data.get('title', '')
        if data.get('description'):
            self.id = data.get('description', '')
        if data.get('itemlist'):
            for item in data.get('itemlist', ''):
                estimate_item:EstimateItem = EstimateItem()
                estimate_item.load_data(data=item)
                self.itemlist.append(estimate_item)
                

