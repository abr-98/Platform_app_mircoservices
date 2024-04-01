class Mail:
    
    def __init__(self, recieversEmail, message, subject):
        self.recieversEmail = recieversEmail
        self.message = message
        self.subject = subject
        
    @staticmethod
    def from_json(json_dict):
        return Mail(json_dict["recieversEmail"],
                    json_dict["message"],
                    json_dict["subject"])