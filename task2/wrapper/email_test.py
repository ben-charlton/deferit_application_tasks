import sendgrid
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Mail, Email, To, Content, Attachment, FileContent, FileName, FileType, Disposition)
import base64

class Email:
    # instantiation of an email object takes in the email address you wish to send emails from
    # and an api key that is attached to the verified email address 
    def __init__(self, fromEmail, apiKey):
        self.fromEmail = fromEmail
        self.apiKey = apiKey

    def send(self, addressTo, subject, message, filePath=None):
        # first build the message and add the attachment if one is given
        # then we use the sendgrid api to send the required email
        # and grab any error messages if they occur
        msg = self._buildMessage(addressTo, subject, message)
        if filePath != None:
            msg.attachment = self._addAttachment(msg, filePath)
        try: 
            sg = SendGridAPIClient(self.apiKey)
            response = sg.send(msg)
            print(response.status_code)
            print(response.headers)
        except Exception as e:
            print(e)

    # the buildMessage function builds the initial Mail object that is sent
    # and attachments are added on later
    def _buildMessage(self, addressTo, subject, message):
        msg = Mail(
            from_email=self.fromEmail,
            to_emails=addressTo,
            subject=subject,
            html_content=Content("text/plain", message)
        )
        return msg

    # the addAttachment function takes in a Mail object
    # and adds an attachment to it under the specified file path
    def _addAttachment(self, email, file_path):
        with open(file_path, 'rb') as f:
            data = f.read()
            f.close()
        encoded_file = base64.b64encode(data).decode()
        attachedFile = Attachment(
            FileContent(encoded_file),
            FileName(os.path.basename(file_path)),
        )
        return attachedFile
    



