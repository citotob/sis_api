from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

def send_mail(subject, text_content, template, d, email_sender, email_receipient):
    htmly     = get_template(template)
    
    html_content = htmly.render(d)
    sender = email_sender
    list_receipient = email_receipient
    msg = EmailMultiAlternatives(
        subject, text_content, sender, list_receipient)
    msg.attach_alternative(html_content, "text/html")
    respone = msg.send()