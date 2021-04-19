import sendgrid
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Mail, Email, To, Content, Attachment, FileContent, FileName, FileType, Disposition)
import base64

class Email:
    def __init__(self):
        pass

    def send(self,address_to, message, file_path=None):
        # build the email to send
        msg = Mail(
            from_email='nothing',
            to_emails=address_to,
            content = Content("text/plain", message)
        )

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
            # Get a JSON-ready representation of the Mail object
            mail_json = mail.get()
            # Send an HTTP POST request to /mail/send
            response = sg.client.mail.send.post(request_body=mail_json)
            print(response.status_code)
            print(response.headers)
        except Exception as e:
            print(e.message)


#test = Email('ben.charlton@hotmail.com.au')
#test.send("ben.charlton@hotmail.com.au", "test")

