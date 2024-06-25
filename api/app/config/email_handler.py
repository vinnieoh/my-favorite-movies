import logging
import smtplib
from email.message import EmailMessage

class EmailHandler(logging.Handler):
    def __init__(self, mailhost, fromaddr, toaddrs, subject, credentials=None, secure=None):
        logging.Handler.__init__(self)
        self.mailhost = mailhost
        self.fromaddr = fromaddr
        self.toaddrs = toaddrs
        self.subject = subject
        self.credentials = credentials
        self.secure = secure

    def emit(self, record):
        try:
            port = self.mailhost[1]
            smtp = smtplib.SMTP(self.mailhost[0], port)
            msg = self.format(record)
            email = EmailMessage()
            email.set_content(msg)
            email['Subject'] = self.subject
            email['From'] = self.fromaddr
            email['To'] = self.toaddrs

            if self.credentials:
                smtp.login(*self.credentials)
            smtp.send_message(email)
            smtp.quit()
        except Exception:
            self.handleError(record)
