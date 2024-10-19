from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

def send_email(subject, template_name, context, recipient_list):
    # Render the HTML template with context data
    html_content = render_to_string(template_name, context)
    msg = EmailMultiAlternatives(subject, "", settings.EMAIL_HOST_USER, recipient_list)
    msg.attach_alternative(html_content, "text/html")  # Attach the HTML content
    msg.send()
