import sendgrid
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Mail, Email, To, Content, Attachment, FileContent, FileName, FileType, Disposition)
import base64

class Email:
    def __init__(self, from_email):
        self.from_email = from_email

    def send(self, address_to, subject, message, file_path=None):
             # build the email to send
        msg = self.buildMessage(address_to, subject, message)
        if file_path != None:
            msg.attachment = self.addAttachment(msg, file_path)
        try: 
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(msg)
            print(response.status_code)
            print(response.headers)
        except Exception as e:
            print(e)

    def buildMessage(self, address_to, subject, message):
        msg = Mail(
            from_email=self.from_email,
            to_emails=address_to,
            subject=subject,
            html_content=Content("text/plain", message)
        )
        return msg

    def addAttachment(self, email, file_path):
        with open(file_path, 'rb') as f:
            data = f.read()
            f.close()
        encoded_file = base64.b64encode(data).decode()
        attachedFile = Attachment(
            FileContent(encoded_file),
            FileName(file_path),
        )
        return attachedFile

# test
test = Email(from_email='ben.charlton@hotmail.com.au')
test.send('bbcharltonn@gmail.com', "testing mail w attachment", "testing mail", '../../task1/MAVG.png')

