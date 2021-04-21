import sendgrid
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Mail, Email, To, Content, Attachment, FileContent, FileName, FileType, Disposition)
import base64

#
# Static class, no object specific member variables needed for Email 
#
class Email:

    @staticmethod
    def send(addressTo, subject, message, filePath=None):
        msg = _buildMessage(addressTo, subject, message)
        if filePath != None:
            msg.attachment = _addAttachment(filePath)
        try: 
            sg = SendGridAPIClient(_getAPIKey())
            response = sg.send(msg)
            print(response.status_code)
            print(response.headers)
        except Exception as e:
            print(e)

    @staticmethod
    def _buildMessage(addressTo, subject, message):
        msg = Mail(
            from_email=_getFromEmail(),
            to_emails=addressTo,
            subject=subject,
            html_content=Content("text/plain", message)
        )
        return msg

    @staticmethod
    def _addAttachment(file_path):
        with open(file_path, 'rb') as f:
            data = f.read()
            f.close()
        encoded_file = base64.b64encode(data).decode()
        attachedFile = Attachment(
            FileContent(encoded_file),
            FileName(os.path.basename(file_path)),
        )
        return attachedFile

    #
    # My first thinking was to include the API key as a class constant, so
    # that SendGridAPI specific details would not be exposed outside of this class,
    # but I have changed to it a private class function, so that if the API key is 
    # updated as an environment variable the code does not have to be re-deployed
    #
    @staticmethod
    def _getAPIKey():
        return os.environ.get('SENDGRID_API_KEY')

    #
    # The from email address is also wrapped within the class. This is because the 
    # from email is attached to the SendGridAPI key, and it cannot be changed independantly.
    # It is also included as an env variable so that if the API key is updated and attached
    # to a new email, the code does not have to be re-deployed
    #
    @staticmethod
    def _getFromEmail():
        return os.environ.get('FROM_EMAIL_ADDRESS')
    