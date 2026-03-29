
from typing import Any
from pydantic import BaseModel, Field, AliasChoices
from modules.utils import generate_id, timestamp
from models.addresslocation_models import Address
from models.comunication_modules import Contact
from models.accounting_models import CommercialAccount, SupplierInvoiceRecord
from models.data_models import ( SupplierStub )


class Supplier(BaseModel):
    id: str = Field(default='', validation_alias=AliasChoices('id', '_id'))
    name:str = Field(default='')     
    taxid: str = Field(default='')
    address:Address = Address()
    contact: Contact = Contact()    
    account:CommercialAccount = CommercialAccount()

    @property
    def _id(self)->str:
        return self.id
    
    @property
    def generate_id(self)->None:
        '''Generates a new supplier Id'''
        if self.name:
            self.id = generate_id(name=self.name)
    

    @property
    def supplier_info(self)->SupplierStub:
        stub:SupplierStub = SupplierStub()
        stub.id = self.id   
        stub.name = self.name
        stub.taxid = self.taxid
        return stub
    

    @property
    def supplier(self):
        data:dict = self.model_dump()
        data['_id'] = self.id
        return data 
    

    def load_data(self, data:dict={}):
        if data:
            if data.get('id'):
                self.id = data.get('id', '')
            elif data.get('_id'):
                self.id = data.get('_id', '')
            if data.get('name'):
                self.name = data.get('name', '')
            if data.get('taxid'):
                self.taxid = data.get('taxid', '')
            if data.get('address'):
                self.address.load_data(data = data.get('address', {}) )
            if data.get('contact'):
                self.contact.load_data(data =  data.get('contact', {}) )
            if data.get('account'):
                self.account.load_data(data = data.get('account', {}))
        else:
            pass 

    def add_invoice_record(self, data:Any=None)->None:
        '''Updates records with a dict or Model'''
        if data:
            if type(data) == dict:
                record:SupplierInvoiceRecord = SupplierInvoiceRecord()
                record.load_data(data = data)
                self.account.transactions.append(record) #TODO Check exist
            elif type(data) == SupplierInvoiceRecord:
                self.account.transactions.append(data)
        else:
            pass
    
    
    
    
    
    
class MaterialSupplier(BaseModel):
    id: str = Field(default="" )
    name:str = Field(default='')     
    taxid: str = Field(default='')
    account:CommercialAccount = CommercialAccount()
    address:Address = Address()
    contact: Contact = Contact()

