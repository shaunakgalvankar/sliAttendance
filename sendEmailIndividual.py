# Code to send email to the entered email address
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(email_address,checkedInHours,possibleHours,dateRangefrom,daterangeTo,student_id):
    # Email configuration
    sender_email = 'shaunakprasad@gmail.com'
    sender_password = 'jfdh hxdc omna opiu'
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    # Create a multipart message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = email_address
    message['Subject'] = student_id+' - SLI Attendance Report'

    # Add body to the email
    body = 'You were checked in for ' + str(checkedInHours) + ' hours out of ' + str(possibleHours) + ' possible hours in the date range ' + str(dateRangefrom) + '-'+str(daterangeTo)+'.'
    message.attach(MIMEText(body, 'plain'))

    # Send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(message)
