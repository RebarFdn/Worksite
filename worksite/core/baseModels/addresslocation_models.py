from pydantic import (BaseModel, Field)

# Address and Location 
class Address(BaseModel):
    lot: str = Field( default= '')
    street: str = Field(default='', min_length=2, max_length=36) 
    town: str = Field(default='', min_length=2, max_length=36)
    city_parish: str = Field(default='', min_length=5, max_length=20)
    country:str = Field(default= '')
    zip: str = Field(default='', min_length=3, max_length=6)
    model_config = {
        "extra": "allow" 
    }

    def load_data(self, data:dict={}):
        if data:
            if data.get('lot'):
                self.lot = data.get('lot', '')
                
            if data.get('street'):
                self.street = data.get('street', '')
                
            if data.get('town'):
                self.town = data.get('town', '')
                
            if data.get('city_parish'):
                self.city_parish = data.get('city_parish', '')
                
            if data.get('country'):
                self.country = data.get('country', '')
                
            if data.get('zip'):
                self.zip = data.get('zip', '')
            if data.get('coords'):
                self.coords.load_data(data = data.get('coords', {}))
            
        else:
            pass
 


class Coords(BaseModel):
    lat:float = Field(default=0.0)  
    lon:float = Field(default=0.0)   
    
    def load_data(self, data:dict={})->None:
        if data:
            if data.get('lat'):
                self.lat = float(data.get('lat', 0.0))
            if data.get('lon'):
                self.lon = float(data.get('lon', 0.0))
        else:
            pass    



class Location(BaseModel):
    coords:Coords = Coords()
    alt:float = Field(default=0.0)
    
    def load_data(self, data:dict={})->None:
        if data:
            if data.get('coords'): # Check for cordinates
                self.coords.load_data(data.get('coords', {})) # Load 
            if data.get('alt'):     # check for altitude
                self.alt = float(data.get('alt', 0.0)) # Assign
        else:
            pass    
    



class AddressLocation(Address):
    coords:Coords = Coords()


