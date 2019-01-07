import smtplib, ssl
import emails.emailcred as cred

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def outage(sites, downCount):
    message = MIMEMultipart("alternative")

    message['Subject'] = '%s Detected Website Outage', [downCount]
    message['From'] = 'EP Uptime Monitor'
    message['To'] = 'njoker555@gmail.com'

    username = cred.EMAIL_CONFIG['username']
    password = cred.EMAIL_CONFIG['password']
    port = 465

    htmlEmail = """
        The following websites have been detected to be down, please check immediately: <br />
        %s 
    """ % (sites)

    emailMsg = MIMEText(htmlEmail, "html")
    message.attach(emailMsg)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(username, password)
        server.sendmail('epuptime@gmail.com', 'njoker555@gmail.com', message)


outage('easyprogramming', '3')

