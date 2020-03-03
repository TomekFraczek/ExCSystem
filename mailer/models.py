import requests

from django.db import models
from django.core.validators import RegexValidator
from django.contrib.postgres.fields import ArrayField

from uwccsystem.settings import EXC_EMAIL, API_BASE, MAILGUN_API_KEY
from mailer import emailing

email_alias = RegexValidator(r'^[0-9a-zA-Z_\-]*$', 'Only letters, numbers, - and _ are allowed')


class EmailList(models.Model):

    name = models.CharField(max_length=20)
    alias = models.CharField(max_length=10, validators=[email_alias])
    description = models.CharField(max_length=100)
    access_level = models.CharField(
        max_length=20,
        choices=(
            ('read-only', 'Default: Only send securely'),
            ('members', 'Allow communication between members'),
            ('everyone', 'Anyone can post')
        ),
        default='read-only'
    )

    emails = ArrayField(models.EmailField())

    def __str__(self):
        return self.email

    @property
    def email(self):
        return f'{self.alias}{EXC_EMAIL}'

    def update_remote(self):

        # Delete the old list
        del_url = f'{API_BASE}/lists/{self.email}'
        del_response = requests.delete(del_url, auth=('api', MAILGUN_API_KEY))

        # Create a new, empty list
        create_url = f'{API_BASE}/lists/'
        create_data = {
            'address': self.email,
            'name': self.name,
            'description': self.description,
            'access_level': self.access_level
        }
        create_response = requests.post(create_url, auth=('api', MAILGUN_API_KEY), data=create_data)

        # Populate the list with all the subscribed email addresses
        fill_url = f'{API_BASE}/lists/{self.email}/members.json'
        fill_response = requests.post(fill_url, auth=('api', MAILGUN_API_KEY), json=self.emails)


class Email(models.Model):

    sender_email = models.EmailField()
    sender_name = models.CharField(max_length=20)

    recipient_single = models.EmailField(blank=True)
    recipient_list = models.ForeignKey(to=EmailList, null=True, on_delete=models.CASCADE)

    subject = models.CharField(max_length=50)
    body = models.TextField()


    @property
    def recipient(self):
        if self.recipient_single:
            email = self.recipient_single
        elif self.recipient_list:
            email = self.recipient_list.email
        else:
            raise ValueError("Email recipient was not defined!")
        return email

    def __repr__(self):
        return emailing.pretty_format_email(
            self.sender_name,
            self.sender_email,
            self.recipient,
            self.subject,
            self.body
        )

    def send(self):
        return emailing.send_email(
            repr(self),
            self.recipient,
            from_email=self.sender_email
        )


