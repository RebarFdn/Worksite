
from pydantic import (BaseModel, EmailStr, Field)
from pydantic_extra_types.phone_numbers import PhoneNumber


from modules.utils import ( generate_id, timestamp )


# Contact and Communication
class Contact(BaseModel):
    """Usage Contact(tel="+18762982925")
    """
    tel: PhoneNumber | None = None
    mobile: PhoneNumber | None = None
    email: EmailStr | None = None
    watsapp: PhoneNumber | None = None
    
    def load_data(self, data:dict={}):
        if data:
            if data.get('tel'):
                self.tel = data.get('tel', '')
            if data.get('mobile'):
                self.mobile = data.get('mobile', '')
            if data.get('email'):
                self.email = data.get('email', '')
            if data.get('watsapp'):
                self.watsapp = data.get('watsapp', '')
            
        else:
            pass


class ReportBody(BaseModel):
    no:int = Field( default=0)
    header:str = Field( default='')
    body:str = Field( default='')
    
    def load_data(self, data:dict={} ):
        if data:
            if data.get('no'):
                self.no = data.get('no', '')
            if data.get('header'):
                self.id = data.get('header', '')
            if data.get('body'):
                self.id = data.get('body', '')
        else:
            pass


class ReportModel(BaseModel):
    id:str = Field(default=generate_id(name='The Report')) 
    author:str = Field(default='')
    date:int = Field(default=timestamp())
    title:str = Field(default='') 
    description:str = Field(default='')
    body_items:list[ReportBody] = []  

    def load_data(self, data:dict={} ):

        if data.get('id'):
            self.id = data.get('id', '')
        if data.get('author'):
            self.author = data.get('author', '')
        if data.get('date'):
            self.date = data.get('date', '')
        if data.get('title'):
            self.id = data.get('title', '')
        if data.get('description'):
            self.id = data.get('description', '')
        if data.get('body_items'):
            for item in data.get('body_items', ''):
                report_body:ReportBody = ReportBody()
                report_body.load_data(data=item)
                self.body_items.append(report_body)

