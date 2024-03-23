import smtplib

from Utility_Module.Mailer.Mailer import Mailer


class MailServiceInfra:
    
    def __init__(self):
        self.email, self.password = Mailer.get_mailer_settings()
        self.mailer = smtplib.SMTP('smtp.gmail.com', 587) 
        self.mailer.starttls()
        self.mailer.login(self.email, self.password)
        
    def SendMail(self,recieversEmail: str, message: str, subject: str):
        mail = self.__CreateMail__(recieversEmail, message, subject)
        self.mailer.sendmail(self.email, recieversEmail, mail)
        
    def __CreateMail__(self, recieversEmail: str, message: str, subject: str):
        mail=\
        f"From: {self.email}\n"+\
        f"To: {recieversEmail}\n"+\
        f"Subject: {subject}\n\n"+\
        f"{message}"
        return mail
        
class MailServiceInfraSingleton:
    
    mailerInstance: MailServiceInfra = None
            
    def GetInstance():
        if MailServiceInfraSingleton.mailerInstance == None:
            MailServiceInfraSingleton.mailerInstance = MailServiceInfra()
            
        return MailServiceInfraSingleton.mailerInstance
    

            
        

