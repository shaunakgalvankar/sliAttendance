# Code to send email to the entered email address
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(email_address):
    # Email configuration
    sender_email = 'shaunakprasad@gmail.com'
    sender_password = 'jfdh hxdc omna opiu'
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    # Create a multipart message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = email_address
    message['Subject'] = 'Subject of the email'

    # Add body to the email
    body = 'This is the body of the email'
    message.attach(MIMEText(body, 'plain'))

    # Send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(message)

send_email("rrajurkar@scu.edu")