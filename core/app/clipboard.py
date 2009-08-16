from __future__ import with_statement

class Clipboard:
    def __init__(self, **kwargs):
        self.data = None
    
    def get_data(self):
        return self.data
        
    def set_data(self,data):
        self.data = data
        return True