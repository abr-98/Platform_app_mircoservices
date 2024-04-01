import logging
from time import sleep

from MailServices.MailEventConsumer import MailEventConsumer

def main():
    logging.basicConfig(filename="app.log", filemode="w", format='%(asctime)s - %(message)s',datefmt= '%d-%b-%y %H:%M:%S')
    logger = logging.getLogger("Mailer")
    mailConsumer : MailEventConsumer = MailEventConsumer(logger)
    mailConsumer.setup()
    
if __name__ == '__main__':
    while True:
        main()
        sleep(0.2)
    