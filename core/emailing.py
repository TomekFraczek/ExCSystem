import re
import smtplib
import sib_api_v3_sdk
from uwccsystem import settings
from django.core.mail.backends.base import BaseEmailBackend
from sib_api_v3_sdk.rest import ApiException


class SendInBlueBackend(BaseEmailBackend):

    def __init__(self, **kwargs):
        self.api_instance = None
        super(SendInBlueBackend, self).__init__()

    @staticmethod
    def parse_email(email_str):

        # Default return
        name = None
        email = email_str

        if "<" in email_str:

            matches = re.search('"([\s\w]*)" <([\s\w@.]*)>', email_str)
            if matches is None:
                print("regex match failed, returning default")

            else:
                try:
                    name = matches.group(1)
                except IndexError:
                    print("No Name Found! Returning default")

                try:
                    email = matches.group(2)
                except IndexError:
                    email = email_str

        parsed = {'email': email}
        if name is not None:
            parsed['name'] = name
        return parsed

    def send_messages(self, email_messages):
        sent = []
        for email in email_messages:
            send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
                to=email.to,
                reply_to=self.parse_email(email.from_email),
                html_content=email.body,
                subject = email.subject
            )
            try:
                api_response = self.api_instance.send_transac_email(send_smtp_email)
            except ApiException as e:
                print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
                if not email.fail_silently:
                    raise e
            else:
                sent.append(api_response)
        return sent

    def open(self):
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = settings.EMAIL_API_KEY
        self.api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    def close(self):
        self.api_instance = None


def send_email(to_emails, title, body,
               from_email=None, from_name=None, receiver_names=None):

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    # Prepare the list of recipients, optionally including names
    if receiver_names is None:
        recipients = [{'email': mail} for mail in to_emails]
    else:
        recipients = [{'email': mail, 'name': name} for name, mail in zip(receiver_names, to_emails)]

    email = {
        "to": recipients,
        "reply_to": {'email': from_email},
        "sender": {
            "name": from_name,
            "email": from_email
        },
        "html_content": body,
        "subject": title
    }

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(**email)

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(api_response)
    except ApiException as e:
        print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
        raise e

