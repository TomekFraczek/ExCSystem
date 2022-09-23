import re
import smtplib
import sib_api_v3_sdk
from uwccsystem import settings
from django.core.mail import send_mail
from django.conf import settings


def email(to_emails, title, body, from_email=None, from_name=None, receiver_names=None):

    # Prepare the list of recipients, optionally including names
    if receiver_names is None:
        recipients = [{'email': mail} for mail in to_emails]
    else:
        recipients = [{'email': mail, 'name': name} for name, mail in zip(receiver_names, to_emails)]

    send_mail(title, body, from_email, recipients)

