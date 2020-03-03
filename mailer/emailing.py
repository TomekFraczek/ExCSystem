import smtplib
import requests
from uwccsystem import settings


def format_recipients(to_emails, receiver_names=None):

    if '@' in to_emails[0]:
        # Prepare the list of recipients, optionally including names
        if receiver_names is None:
            recipients = ", ".join([f'<{email}>' for email in to_emails])
        else:
            recipients = ", ".join([f'{receiver[0]} <{receiver[1]}>' for receiver in zip(receiver_names, to_emails)])
    else:
        # Handle the case when we were given just a single recipient
        if to_emails:
            recipients = f'{receiver_names} <{to_emails}>'
        else:
            recipients = to_emails

    return recipients


def pretty_format_email(from_name, from_email, recipients, title, body):
    """Prepare the formatted email message ready to be sent"""
    return f"From: {from_name} <{from_email}> \n" \
        f"To: {recipients} \n" \
        f"Subject: {title} \n" \
        f"{body} \n"


def send_email(ready_email, to_emails, from_email=None, host_email=None, smtp_password=None):

    # If SMTP credentials are not given, use defaults
    from_email = from_email if from_email else settings.EMAIL_HOST_USER
    host_email = host_email if host_email else settings.EMAIL_HOST_USER
    smtp_password = smtp_password if smtp_password else settings.EMAIL_HOST_PASSWORD

    smtp_obj = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    if settings.EMAIL_USE_TLS:
        smtp_obj.starttls()
        smtp_obj.login(host_email, smtp_password)
    smtp_obj.sendmail(from_email, to_emails, ready_email)


def send_membership_email(to_emails, title, body, receiver_names=None):
    """Send an email from the club membership email. See send_email for more details"""
    from_name = 'Membership | CCUW'
    recipients = format_recipients(to_emails, receiver_names)
    ready_email = pretty_format_email(
        from_name,
        settings.MEMBERSHIP_EMAIL_HOST_USER,
        recipients,
        title,
        body
    )
    send_email(
        ready_email,
        to_emails,
        host_email=settings.MEMBERSHIP_EMAIL_HOST_PASSWORD,
        smtp_password=settings.MEMBERSHIP_EMAIL_HOST_PASSWORD,
    )


def create_staffer_forward(club_email, full_name, forward_email):

    route_data = {
        'description': f'Email forwarding for Staffer: {full_name}',
        'match': f"match_recipient('{club_email}')",
        'action': f"forward('{forward_email}')",
    }

    url = f'{settings.API_BASE}/routes'
    response = requests.post(url, auth=('api', settings.MAILGUN_API_KEY), data=route_data)
    return response


