from typing import List, Any

from pydantic import BaseModel, EmailStr, Field,  SecretStr, AliasChoices, ValidationError
from pydantic_extra_types.country import CountryShortName 
from pydantic_extra_types.phone_numbers import PhoneNumber

try:
    from modules.utils import generate_id, timestamp, datimestamp, convert_timestamp, tally, convert_price_by_unit,convert_unit
except ImportError:
    from utils import generate_id, timestamp, datimestamp, convert_timestamp, tally, convert_price_by_unit,convert_unit



# Password Model
class Password(BaseModel):
    password: SecretStr = Field(
        default=None, min_length=6, max_length=12,
        json_schema_extra={"icon": "shield", "help": "Password should be between 6 and 12 letters."} 
    )
    def validate(self, value:Any) -> Any:
        try:
            model = Password( **value )
        except ValidationError as ero:
            error_locations = ero
            return error_locations
        return value
    

# Registration Model
class User(BaseModel):
    name: str = Field(default='', min_length=3, max_length=32)
    username: str = Field(default='', min_length=3, max_length=8)
    email: EmailStr = ''
    
    def load_data(self, data:dict={}):
        if data:
            if data.get('name'):
                self.name = data.get('name', '')
            if data.get('username'):
                self.username = data.get('username', '')
            if data.get('email'):
                self.email = data.get('email', '')
        else:
            pass


# Registration Model
class RegisterUser(BaseModel):
    name: str = Field(default='', min_length=3, max_length=32)
    username: str = Field(default='', min_length=3, max_length=8)
    email: EmailStr = ''
    password:SecretStr = Field(
        default=None, min_length=6, max_length=12,
        json_schema_extra={"icon": "shield", "help": "Password should be between 6 and 12 letters."} 
    )
    

    def validate(self, value:Any) -> Any:
        try:
            model = RegisterUser( **value )
        except ValidationError as ero:
            error_locations = ero.errors
            return error_locations
        return value

