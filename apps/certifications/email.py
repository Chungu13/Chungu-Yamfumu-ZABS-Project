from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone

def send_status_email(application):
    subject = 'Certification Application Status Update'
    html_message = render_to_string('email_template.html', {'application': application, 'current_year': timezone.now().year})
    plain_message = strip_tags(html_message)  # This strips the HTML tags for plain text fallback
    from_email = 'certifications@yourcompany.com'
    to = application.manufacturer.user.email  # Send the email to the manufacturer
    

    send_mail(subject, plain_message, from_email, [to], html_message=html_message)
