class Mail:
    
    def __init__(self, recieversEmail, message, subject):
        self.recieversEmail = recieversEmail
        self.message = message
        self.subject = subject
        
    @staticmethod
    def from_json(json_dict):
        return Mail(json_dict["Reciever"],
                    json_dict["Message"],
                    json_dict["Subject"])