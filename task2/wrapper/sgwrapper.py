import sendgrid
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Mail, Email, To, Content, Attachment, FileContent, FileName, FileType, Disposition)
import base64

class Email:
    def __init__(self):
        pass

    def send(address_to, message, file_path=None):
        # build the email to send
        msg = Mail(
            from_email='from_email@example.com',
            to_emails=address_to,
            content = Content("text/plain", message)

        # if there is an attachment, add it to the email
        if file_path != None:
            with open(file_path, 'rb') as f:
                data = f.read()
                f.close()
            encoded_file = base64.b64encode(data).decode()
            attachedFile = Attachment(
                FileContent(encoded_file),
                FileName(file_path),
                Disposition('attachment')
            )
            msg.attachment = attachedFile
        
        try: 
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(msg)
            print(response.status_code, response.body, response.headers)
        except Exception as e:
            print(e.message)



    