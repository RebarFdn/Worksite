
from datetime import ( datetime, )
from pydantic import ( BaseModel, Field )
from core.utilities.utils import ( timestamp, convert_timestamp )


# States
class State(BaseModel):
    active:bool = False
    complete:bool = False
    pause:bool = False
    terminate:bool = False
    
    def load_data(self, data:dict={})->None:
        if data:
            # process active state
            if data.get('active'):
                self.active = data.get('active', False)
            elif data.get('activate'):
                self.active = data.get('activate', False)
            # process completion state
            if data.get('complete'):
                self.complete = data.get('complete', False)
            if data.get('pause'):
                self.pause = data.get('pause', False)
            if data.get('terminate'):
                self.terminate = data.get('terminate', False)               
        else:
            pass
                              
    def set_state(self, state:str):
        """
        Updates the state of an object, 
        a change in one state affects other states.
        
        :param state: the object's state to be updated
        :type state: str
        """
        if state == 'activate':
            self.active = True
            self.complete = False
            self.pause = False
            self.terminate = False
            
        elif state == 'complete':
            self.active = False
            self.complete = True
            self.pause = False
            self.terminate = False
            
        elif state == 'pause':
            self.active = False
            self.complete = False
            self.pause = True
            self.terminate = False
            
        elif state == 'terminate':
            self.terminate = True
            self.active = False
            self.complete = False
            self.pause = False
            self.terminate = True
            
        elif state == 'resume':
            self.active = True
            self.active = False
            self.complete = False
            self.pause = False
            self.terminate = False
          

class Event(BaseModel):
    created:int = 0 # timestamp
    started:int = 0 # timestamp
    completed:int = 0
    paused:list = []
    restart:list = []
    terminated: int = 0
    duration:int = 0

    def load_data(self, data:dict={}):
        if data:
            if data.get('created'):
                self.created = timestamp(data.get('created', ''))
            if data.get('started'):
                self.started = timestamp(data.get('started', ''))
                
            if data.get('completed'):
                 self.completed = timestamp(data.get('completed', ''))
    
            if data.get('paused'):
                 self.paused = data.get('paused',[])
    
            if data.get('restart'):
                 self.restart = data.get('restart', [])
    
            if data.get('terminated'):
                 self.terminated = timestamp(data.get('terminated', ''))    
    
            self.update_duration              
        else:
            pass
        
    def update_event(self, event:str, event_date:str | None = None ):
        '''
        Uptates event date. If no date is provided will default to the current date.
        
        :param event: the event to be updated
        :type event: str
        :param event_date: The date that the event ocured "2026-02-08"
        :type event_date: str
        '''
        if not event_date:
            event_date = datetime.now().strftime("%Y-%m-%d")

        if event == 'create':
            self.created = timestamp(date=event_date)
        if event == 'activate':
            self.started = timestamp(date=event_date)
        elif event == 'complete':
            self.completed = timestamp(date=event_date)
        elif event == 'pause':
            self.paused.append(timestamp(date=event_date))
        elif event == 'resume':
            self.restart.append(timestamp(date=event_date))
        elif event == 'terminate':
            self.terminated = timestamp(date=event_date)
        self.update_duration  
    
    @property
    def update_duration(self):
        format_string = "%Y-%m-%d"
        dt1 = datetime.strptime(convert_timestamp(self.started), format_string)
        dt2 = datetime.strptime(convert_timestamp(self.completed), format_string)
        # Calculate the difference (timedelta object)
        diff =  dt2 - dt1
        self.duration = diff.days



class StopWatchEvent(BaseModel):
    started:int = Field( default=0 ) # timestamp
    updated:int = Field( default=0 )
    duration:int = Field( default=0 )   

    def load_data(self, data:dict={}):
        if data:
            if data.get('started'):
                self.started = data.get('started', 0)
                
            if data.get('updated'):
                 self.updated = data.get('upated', 0)                          
        else:
            pass
        
    def update_event(self, event:str, event_date:str=''):
        '''
        Uptates event date. If no date is provided will default to the current date.
        
        :param event: the event to be updated
        :type event: str
        :param event_date: The date that the event ocured "2026-02-08"
        :type event_date: str
        '''
        if not event_date:
            event_date = datetime.now().strftime("%Y-%m-%d")

        if event == 'started':
            self.started = timestamp(date=event_date)
        elif event == 'updated':
            self.updated = timestamp(date=event_date)
        
        self.update_duration  
    
    @property
    def update_duration(self):
        format_string = "%Y-%m-%d"
        dt1 = datetime.strptime(convert_timestamp(self.started), format_string)
        dt2 = datetime.strptime(convert_timestamp(self.updated), format_string)
        # Calculate the difference (timedelta object)
        diff =  dt2 - dt1
        self.duration = diff.days


class ComonActionModel(BaseModel):
    archived:bool = Field(default=False)
    cloned:bool = Field(default=False) # if object was cloned
    locked:bool = Field(default=False) # places oject in readonly mode
    shared:bool = Field(default=False) # if there is collaboration  
    
    def load_data(self, data:dict = {})->None:
        if data:
            self.archived = data.get('archived', False)
            self.cloned = data.get('cloned', False)
            self.locked = data.get('locked', False)
            self.shared = data.get('shared', False)

        else:
            pass
                
