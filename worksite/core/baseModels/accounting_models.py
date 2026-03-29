from typing import ( Any, )

from pydantic import ( BaseModel, Field, AliasChoices )
from core.utilities.utils import ( generate_id, timestamp, tally )

from core.baseModels.measurments_models import (MetricModel, ImperialModel)
from core.baseModels.data_models import ( SupplierStub )



class Recipient(BaseModel):
    name:str = Field(default='')
    def load_data(self, data:dict={})->None:
        if data:
            if data.get('name'):
                self.name = data.get('name', '')
        else:
            pass



class ComercialRecipient(BaseModel):
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
    

    

## Financial and Accounting Models
class Bank(BaseModel):
    name: str = Field(default='', min_length=2, max_length=32) 
    branch: str = Field(default='', min_length=2, max_length=32)
    account: str = Field(default='', min_length=2, max_length=16)
    account_type: str = Field(default="savings",  max_length=16)
    holder: str = Field(default="",  max_length=32)

    
    def load_data(self, data:dict={} ):
        if data:
            if data.get('name'):
                self.name = data.get('name', '')
            if data.get('branch'):
                self.branch=data.get('branch', '')
            if data.get('account'):
                self.account = data.get('account', '')
            if data.get('account_type'):
                self.account_type = data.get('account_type', '')
            if data.get('holder'):
                self.holder = data.get('holder', '')
        else:
            pass



class CommercialAccount(BaseModel):
    bank: Bank = Bank() 
    transactions: list[ Any ] = []

    def load_data(self, data:dict={}):
        if data:
            if data.get('bank'):
                self.bank.load_data(data=data.get('bank', {}))
            if data.get('transactions'):
                for item in data.get('transactions', []):
                    #record:SupplierInvoiceRecord = SupplierInvoiceRecord()
                    #record.load_data(data=item)
                    self.transactions.append(item)

        else:
            pass



class DepositModel(BaseModel):
    id:str = Field(default=generate_id(name='account deposit') )
    date:int = Field(default=timestamp())
    type:str = Field(default="deposit")
    ref:str = Field(default="")
    amount:float =Field(default=0.001)
    payee:str = Field(default="")
    user:str = Field(default="ian")
    
    def load_data(self, data:dict={})->None:
        ''' Load existing deposit data into the Model '''
        if data:
            if data.get('id'):
                self.id = data.get('id', '')
            if data.get('date'):
                self.date = timestamp(data.get('date', ''))
            if data.get('type'):
                self.type = data.get('type', 'withdrawal')
            if data.get('ref'):
                self.ref = data.get('ref', '')
            if data.get('amount'):
                self.amount = float(data.get('amount', ''))
            if data.get('payee'):
                self.payee = data.get('payee', '')               
            if data.get('user'):
                self.user = data.get('user', '')
        else:
            pass
 


class WithdrawalModel(BaseModel):
    id:str = Field(default=generate_id(name='account withdraw') )
    date:int = Field(default=timestamp())
    type:str = Field(default="withdrawal")
    ref:str = Field(default="")
    amount:float =Field(default=0.001)
    recipient:Recipient = Recipient()
    user:str = Field(default="system")

    def load_data(self, data:dict={})->None:
        ''' Load existing withdrawal data into the Model '''
        if data:
            if data.get('id'):
                self.id = data.get('id', '')
            if data.get('date'):
                self.date = timestamp(data.get('date', ''))
            if data.get('type'):
                self.type = data.get('type', 'withdrawal')
            if data.get('ref'):
                self.ref = data.get('ref', '')
            if data.get('amount'):
                self.amount = float(data.get('amount', ''))
            if data.get('recipient'):
                if type(data.get('recipient')) == str:
                    self.recipient.name = data.get('recipient', '')
                else:
                    self.recipient.load_data(data = data.get('recipient', {}))
            if data.get('user'):
                self.user = data.get('user', '')
        else:
            pass
 


class AccountTransactions(BaseModel):
    deposit:list[DepositModel] = []
    withdraw:list[WithdrawalModel] = []

    def load_data(self, data:dict ={})->None:
        if data:
            if data.get('deposit') and len(data.get('deposit', [])) > 0:
                for item in data.get('deposit', []):
                    deposit = DepositModel()
                    deposit.load_data(data=item)
                    self.deposit.append(deposit)
                
            if data.get('withdraw') and len(data.get('withdraw', [])) > 0:
                for item in data.get('withdraw', []):
                    withdrawal = WithdrawalModel()
                    withdrawal.load_data(data=item)
                    self.withdraw.append(withdrawal)
        else:
            pass
    
    #Indexes
    ## Withdraw index
    @property
    def withdraw_index(self):
        pass
    
    def add_withdrawal(self, data:WithdrawalModel=WithdrawalModel())->None:
        # check exist 
        search:list = [withdrawal for withdrawal in self.withdraw if withdrawal.ref == data.ref and withdrawal.date == data.date and withdrawal.recipient == data.recipient ]

        if search:
            pass
        else:
            self.withdraw.append(data)


class Loan( BaseModel ):
    id: str = Field( default=generate_id(name='Bank Loan') )
    date:int = Field(default= timestamp()) 
    amount:float = Field(default=0.00, max_digits=5)
    borrower: str = Field(default='', min_length=2, max_length=32)
    refference:str = Field(default='', min_length=2, max_length=8)
    
    def load_data(self, data:dict={})->None:
        if data:
            if data.get('id'):
                self.id = data.get('id', '')
            if data.get('date'):
                self.date = timestamp(data.get('date', ''))
            if data.get('amount'):
                self.amount = float(data.get('amount', ''))
            if data.get('borrower'):
                self.borrower = data.get('borrower', '')
            if data.get('refference'):
                self.refference = data.get('refference', '')
        else:
            pass
    

class LoanPayment( BaseModel ):
    id: str = Field( default=generate_id(name='Bank Loan') )
    date:int = Field( default=timestamp() )
    amount:float = Field(default=0.0)
    payee:str = Field(default='')
    refference:str = Field(default='')
    
    def load_data(self, data:dict={})->None:
        if data:
            if data.get('id'):
                self.id = data.get('id', '')
            if data.get('date'):
                self.date = timestamp(data.get('date', ''))
            if data.get('amount'):
                self.amount = float(data.get('amount', ''))
            if data.get('borrower'):
                self.borrower = data.get('borrower', '')
            if data.get('refference'):
                self.refference = data.get('refference', '')
        else:
            pass


class InvoiceItem(BaseModel):
    invoiceno:str = Field(default='') 
    iid:str = Field(default=generate_id(name='invoice item'))
    itemno:int = Field(default=0)  
    description:str = Field(default='') 
    quantity:float = Field(default=0.01) 
    unit:str = Field(default='') 
    price:float = Field(default=0.01)    

    def load_data(self, data:dict={}):
        if data:
            if data.get('invoiceno'):
                self.invoiceno = data.get('invoiceno', '')
            if data.get('itemno'):
                self.itemno = int(data.get('itemno', 0))
            if data.get('description'):
                self.description = data.get('description', '')
            if data.get('quantity'):
                self.quantity = float(data.get('quantity', 0.0))
            if data.get('unit'):
                self.unit = data.get('unit', '')
            if data.get('price'):
                self.price = float(data.get('price', 0.0))
            
        else:
            pass 
    
    
    
class InvoiceModel(BaseModel):
    id: str = Field(default=generate_id(name='purchase invoice'))
    supplier:SupplierStub = SupplierStub()
    invoiceno:str = Field(default= '') 
    date:int = Field(default=timestamp()) 
    items:list[InvoiceItem] = []
    tax:float = Field(default=0.001) 
    total:float = Field(default=0.001) 
    billed:bool = Field(default=False) 

    def load_data(self, data:dict={}):
        if data:
            if data.get('inv_id'):
                self.id = data.get('inv_id', '')
            elif data.get('id'):
                self.id = data.get('id', '')
            
            if data.get('supplier'):
                self.supplier.load_data(data= data.get('supplier', {}))
            if data.get('invoiceno'):
                self.invoiceno = data.get('invoiceno', '')
            if data.get('date'):
                self.date = timestamp(data.get('date', ''))
            if data.get('items'):
                for item in data.get('items', []):
                    inv_item:InvoiceItem = InvoiceItem()
                    inv_item.load_data(data=item)
                    self.items.append(inv_item) 
                
            if data.get('tax'):
                self.tax = float(data.get('tax', 0))
            if data.get('total'):
                self.total = float(data.get('total', 0))
            if data.get('billed'):
                self.billed = data.get('billed', False)
        else:
            pass 

    def add_item(self, form_data:dict={})->None:
        item:InvoiceItem = InvoiceItem()
        if form_data:
            if form_data.get('description'):
                if form_data.get('description') in self.invoice_description_index :
                    pass
                else:
                    if form_data.get('invoiceno'):
                        item.invoiceno = form_data.get('invoiceno', '')                    
                    if form_data.get('description'):
                        item.description = form_data.get('description', '')
                    if form_data.get('quantity'):
                        item.quantity = float(form_data.get('quantity', 0.0))
                    if form_data.get('unit'):
                        item.unit = form_data.get('unit', '')
                    if form_data.get('price'):
                        item.price = float(form_data.get('price', 0.0))
                   
                    item.itemno = len(self.items)+ 1
            
                    self.items.append(item)

        else:
            pass
    
    @property
    def invoice_description_index(self)->list:
        return [item.description for item in self.items ]
    
    

class SupplierInvoiceRecord(BaseModel):
    '''Record of a transaction with with a supplier,
    
    .. Is stored on the supplier's data 
    '''
    inv_id: str = Field(default='')   
    invoiceno:str = Field(default= '') 
    date:int = Field(default=timestamp() )    
    total:float = Field(default=0.00) 

    def load_data(self, data:dict={}):
        if data:
            if data.get('inv_id'):
                self.inv_id = data.get('inv_id', '')
            if data.get('invoiceno'):
                self.invoiceno = data.get('invoiceno', '')
            if data.get('date'):
                self.date = timestamp(data.get('date', ''))
            if data.get('total'):
                self.total = float(data.get('total', 0.0) )
        else:
            pass 

 
# Account Paybill related models
class BillExpence(BaseModel):
    contractor:float = Field(default=0.001)
    insurance:float = Field(default=0.001)
    misc:float = Field(default=0.001)
    overhead:float = Field(default=0.001)
    total:float = Field(default=0.001)

    def load_data(self, data:dict={})->None:
        ''' Load existing  data into the Model '''
        if data:            
            if data.get('contractor'):
                self.contractor = float(data.get('contractor', ''))
            if data.get('insurance'):
                self.insurance = float(data.get('insurance', ''))
            if data.get('misc'):
                self.misc = float(data.get('misc', ''))
            if data.get('overhead'):
                self.overhead = float(data.get('overhead', ''))
            self.calculate_total
        else:
            pass

    @property
    def calculate_total(self)->None:
        self.total = round( sum( [ self.contractor, self.insurance, self.misc, self.overhead ] ), 2 )
 

class BillFees(BaseModel):
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



class UnpaidTaskModel(BaseModel):
    id:str = Field(default='', validation_alias=AliasChoices('id', '_id'))
    job_id:str = Field(default='')
    title:str = Field(default='')
    metric:MetricModel = MetricModel()
    imperial:ImperialModel = ImperialModel()
    assignedto:Any = Field(default=None)
    progress: int =  Field(default=0)
    total:float= Field(default=0.001)

    @property
    def set_quantity_percent(self)->None:
        if self.progress > 0:
            percent = self.progress / 100
            self.metric.quantity = self.metric.quantity * percent
            self.metric.calculate_total
            self.imperial.quantity = self.imperial.quantity * percent
            self.imperial.calculate_total
        self.calculate_total

    @property
    def calculate_total(self):
        if self.metric.total > 0.001:
            self.total = self.metric.total
        elif self.imperial.total > 0.001:
            self.total = self.imperial.total
    
 

class Payment(BaseModel):
    amount:float = 0.0
    deductions:float = 0.0
    total: float = 0.0
    
    def load_data(self, data:dict={}):
        if data:
            if data.get('amount'):
                self.amount = float(data.get('amount', 0.0))
            if data.get('deductions'):
                self.deductions = float(data.get('deductions', 0.0))
            self.calculate_total
        else:
            pass 
        
    @property
    def calculate_total(self)->None:
        self.total = self.amount - self.deductions


    def update_amount(self, figure:float=0.0):
        self.amount = self.amount + figure
        self.calculate_total

   
class PayItem(BaseModel):
    no:int = 0
    id:str = Field(default='')
    job_id:str = Field(default='')
    title:str = Field(default='') 
    description:str = Field(default='')   
    metric:MetricModel = MetricModel()
    imperial:ImperialModel = ImperialModel()
    progress:int = Field(default=0)
    total:float = Field(default=0.0)

    def load_data(self, data:dict={}):
        if data:
            if data.get('no'):
                self.no = int(data.get('no', 0))
            if data.get('id'):
                self.id = data.get('id', '')
            if data.get('job_id'):
                self.job_id = data.get('job_id', '')
            if data.get('title'):
                self.title = data.get('title', '')             
            if data.get('metric'):
                self.metric.load_data(data.get('metric', {}))
                self.metric.calculate_total
            if data.get('imperial'):
                self.imperial.load_data( data.get('imperial', {}) )
                self.imperial.calculate_total
            if data.get('progress'):
                self.progress = int(data.get('progress', 0))
            if data.get('total'):
                self.total = float(data.get('total', 0.0))
        else:
            pass 
          
    @property
    def calculate_total(self): 
        self.metric.calculate_total
        self.imperial.calculate_total    
   


class PayStatement(BaseModel):
    """Employee Pay Statement is a record of payment 
    for tasks , stored on the employee's records.
    """
    id:str = Field(default=generate_id(name='Pay statement') )
    project:str = Field(default='')
    bill_ref:str = Field(default='')
    employee_id:str = Field(default='')
    date:int = Field(default=timestamp())
    items:list[PayItem] = []
    payment:Payment = Payment()
    
    @property 
    def item_ids(self)->list[str]:
        return [ item.id for item in self.items ]

    def load_data(self, data:dict={}):
        if data:
            if data.get('id'):
                self.id = data.get('id', '')
            if data.get('project'):
                self.project = data.get('project', '')
            if data.get('bill_ref'):
                self.bill_ref = data.get('bill_ref', '')
            if data.get('employee_id'):
                self.employee_id = data.get('employee_id', '')
            if data.get('date'):
                self.date = timestamp(data.get('date', ''))
            if data.get('items'):
                for item in data.get('items', []):
                    if item:
                        pay_item = PayItem()
                        pay_item.load_data( data=item )
                        self.items.append(pay_item)                        
            if data.get('payment'):
                self.payment.load_data( data=data.get('payment', ''))            
        else:
            pass  

        
    def add_payitem(self, item:PayItem):
        item.no = len(self.items)  + 1
        item.calculate_total        
        self.items.append(item)
        if item.metric.total > 0.01:
            self.payment.amount =  self.payment.amount + item.metric.total
        elif item.imperial.total > 0.01:
            self.payment.amount = self.payment.amount + item.imperial.total
        self.payment.calculate_total
        




class PaybillItem(BaseModel):
    ''' '''
    id:str = Field(default='')
    job_id:str = Field(default='')
    title:str = Field(default='')    
    metric:MetricModel = MetricModel()
    imperial:ImperialModel = ImperialModel()
    assignedto:list[str] = []
    progress:int = Field(default=0)
    total:float = Field(default=0.0)

    def load_data(self, data:dict={}):
        if data:            
            if data.get('id'):
                self.id = data.get('id', '')
            if data.get('title'):
                self.title = data.get('title', '')            
            if data.get('metric'):
                self.metric.load_data(data.get('metric', {}))
                self.metric.calculate_total
            if data.get('imperial'):
                self.imperial.load_data( data.get('imperial', {}) )
                self.imperial.calculate_total
            if data.get('assignedto'):
                self.assignedto = data.get('assignedto', [])
            if data.get('progress'):
                self.progress = int(data.get('progress', 0))
            if data.get('total'):
                self.total = float(data.get('total', 0.0))
        else:
            pass 
          
    @property
    def calculate_total(self): 
        return self.metric.total

    @property
    def set_jobid(self):
        if self.id and '-' in self.id:
            self.job_id = self.id.split('-')[0]   
   


class PaybillModel(BaseModel):
    id:str = Field(default=generate_id(name='pay bill') ) # Bill internal id
    ref:str = Field(default='')   # Bill to job refference no
    project_id:str = Field(default='') # Current project _id
    date:int = Field(default=timestamp())  # Paybill generation date
    date_starting:int = Field(default=timestamp()) # Work period starting
    date_ending:int = Field(default=timestamp())   # Work period ending
    mainTitle:str = Field(default='') # Bill heading
    subTitle:str = Field(default='')  # Bill sub headings
    itemsTotal:float = Field(default=0.001)   # Bill items total
    total:float = Field(default=0.001)   # Bill Total
    items:list[PaybillItem] = []    
    days_work:list = []
    user:str = Field(default="Ian")
    expence:BillExpence = BillExpence()
    fees:BillFees = BillFees()

    @property
    def calculate_total(self):
        self.calculate_items_total 
        self.calculate_expence

        self.total = self.itemsTotal + self.expence.total

    @property
    def calculate_items_total(self):
        self.itemsTotal = tally( items=[item.model_dump() for item in self.items] )

    @property
    def calculate_expence(self):
        if self.fees.contractor > 0:
            self.expence.contractor = self.itemsTotal * (self.fees.contractor / 100)
        else:
            pass
        if self.fees.insurance > 0:
            self.expence.insurance = self.itemsTotal * (self.fees.insurance / 100)
        else:
            pass
        if self.fees.misc > 0:
            self.expence.misc = self.itemsTotal * (self.fees.misc / 100)
        else:
            pass
        if self.fees.overhead > 0:
            self.expence.overhead = self.itemsTotal * (self.fees.overhead / 100)
        else:
            pass
        self.expence.total = sum([self.expence.contractor, self.expence.insurance, self.expence.misc, self.expence.overhead ])


    @property
    def item_ids(self):
        return [ item.id for item in self.items ]
    
    @property
    def employee_ids(self)->list[str]:
        ids = set()
        for bill_item in self.items:
            if bill_item.assignedto:
                for worker in bill_item.assignedto:
                    ids.add(worker)
        return list(ids)


    def load_data(self, data:dict={}):
        if data:
            if data.get('id'):
                self.id = data.get('id', '')
            if data.get('ref'):
                self.ref = data.get('ref', '')
            if data.get('project_id'):
                self.project_id = data.get('project_id', '')
            if data.get('date'):
                self.date = data.get('date', '')
            if data.get('date_starting'):
                self.date_starting = data.get('date_starting', '')
            if data.get('date_ending'):
                self.date_ending = data.get('date_ending', '')
            if data.get('mainTitle'):
                self.mainTitle = data.get('mainTitle', '')
            if data.get('subTitle'):
                self.subTitle = data.get('subTitle', '')
            if data.get('itemsTotal'):
                self.itemsTotal = data.get('itemsTotal', '')
            if data.get('total'):
                self.total = data.get('total', '')
            if data.get('items'):
                for item in data.get('items', []):
                    bill_item:PaybillItem = PaybillItem()
                    bill_item.load_data(data=item)
                    bill_item.set_jobid
                    self.items.append(bill_item)
            if data.get('days_work'):
                self.days_work = data.get('days_work', '')
            if data.get('user'):
                self.user = data.get('user', '')
            if data.get('expence'):
                self.expence.load_data(data = data.get('expence', {}))
                self.expence.calculate_total
            if data.get('fees'):
                self.fees.load_data(data = data.get('fees', {}))
            self.calculate_total
        else:
            pass
                
    
    def add_item(self, data:dict={}):
        if data:
            if data.get('id') in self.item_ids:
                pass
            else:
                bill_item:PaybillItem = PaybillItem()
                bill_item.load_data(data=data)
                self.items.append(bill_item)

    def get_paybill_item(self, item_id:str=''):
        if item_id in self.item_ids:
            return [ item for item in self.items if item.id == item_id ][0]
        return PaybillItem()
                   
            
class DayPay(BaseModel):
    amount:float = Field(default=0.0)
    rate:float = Field(default=0.0)
    paid:bool = Field(default=False)

    def load_data(self, data:dict={} ):
        if data:

            if data.get('amount'):
                self.amount = data.get('amount', 0.0)

            if data.get('rate'):
                self.rate = data.get('rate', 0.0)

            if data.get('paid'):
                self.paid = data.get('paid', False)
            else:
                pass

