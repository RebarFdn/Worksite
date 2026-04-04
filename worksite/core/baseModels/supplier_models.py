
from typing import Any
from pydantic import BaseModel, Field, AliasChoices
from core.utilities.utils import generate_id, timestamp
from core.baseModels.addresslocation_models import Address
from core.baseModels.comunication_modules import Contact
from core.baseModels.accounting_models import CommercialAccount, SupplierInvoiceRecord
from core.baseModels.data_models import ( MetaData, SupplierStub )



class Supplier(BaseModel):
    id: str = Field(default='', validation_alias=AliasChoices('id', '_id'))
    name:str = Field(default='')     
    taxid: str = Field(default='')
    address:Address = Address()
    contact: Contact = Contact()    
    account:CommercialAccount = CommercialAccount()
    metadata:MetaData = MetaData()

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

    
    def load_form_data(self, form_data:dict={}):
        if form_data:            
            if form_data.get('name'):
                self.name = form_data.get('name', '')
            if form_data.get('taxid'):
                self.taxid = form_data.get('taxid', '')
            if form_data.get('street') or form_data.get('city_parish') or form_data.get('country') or form_data.get('zip'):
                self.address.load_data( data=form_data )
            if form_data.get('tel') or form_data.get('email') or form_data.get('mobile'):
                self.contact.load_data( data=form_data )
            if form_data.get('account'):
                del form_data['name']
                self.account.bank.load_data( data=form_data )
                
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
    
 
    
    
class MaterialSupplier(Supplier):
    materials:list = Field(default_factory=list)

