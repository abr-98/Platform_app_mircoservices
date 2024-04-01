import datetime as dt
import threading 

class IdGenerator:
    
    def __init__(self):
        self.count = 0 
    
    def GenerateUniqueId(self):
        string = str(dt.datetime.now())
        datetime = ''.join(e for e in string if e.isalnum())
        threadid = threading.get_ident()
        
        return f"{datetime}:{threadid}:{str(self.count).zfill(12)}"
        
        
        
        