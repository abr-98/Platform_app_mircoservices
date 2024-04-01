import smtplib
import logging
from MailServices.MailExceptions import MailException
from MailServices.Mailer import Mailer

logging.basicConfig(filename="app.log", filemode="w", format='%(asctime)s - %(message)s',datefmt= '%d-%b-%y %H:%M:%S')

class MailServiceInfra:
    
    def __init__(self):
        self.email, self.password = Mailer.get_mailer_settings()
        self.mailer = smtplib.SMTP('smtp.gmail.com', 587) 
        self.mailer.starttls()
        self.mailer.login(self.email, self.password)
        
    def SendMail(self,recieversEmail: str, message: str, subject: str):
        try:
            mail = self.__CreateMail__(recieversEmail, message, subject)
            self.mailer.sendmail(self.email, recieversEmail, mail)
            logging.info(f"Mail sent to {recieversEmail}")
        except Exception as e:
            logging.error(str((MailException.WhenMailDispatchFails(e)).ex))
        
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
    

            
        

