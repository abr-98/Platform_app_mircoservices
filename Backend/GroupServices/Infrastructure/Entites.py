class Entities:
    
    def __init__(self,id, name, interests: str, type):
        self.id = id
        self.name = name
        self.interests = interests
        self.type = type
        
    @staticmethod
    def From(id, name, interests, type):
        return Entities(id, name, interests, type)
    
    
    @staticmethod
    def from_json(json_dict):
        return Entities(json_dict["id"],json_dict["name"], json_dict["interest"], json_dict["type"])