import smtplib, ssl
import config.config as cred

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import db

global downSites
downSites = []


def outage(sites, downCount):

    # Config values
    username = cred.EMAIL_CONFIG['username']
    password = cred.EMAIL_CONFIG['password']
    port = cred.EMAIL_CONFIG['port']
    smtpServer = cred.EMAIL_CONFIG['smtpServer']
    sender = cred.EMAIL_CONFIG['sender']
    recipient = cred.EMAIL_CONFIG['recipient']

    msg = MIMEMultipart("alternative")
    msg['Subject'] = 'Website outage detected!'
    msg['From'] = 'EP Uptime Monitor'
    msg['To'] = recipient

    html = """
        The following websites have been detected to be down, please check the %s website(s) immediately: <br />
    """ % (downCount)

    html += "<ul>"
    for site in sites:
        html += """
            <li>%s - check failed %s times</li> 
        """ % (site['site'], site['downCount'])
        downSites.append(site['site'])
    html += "</ul>"

    emailMsg = MIMEText(html, "html")

    msg.attach(emailMsg)

    context = ssl.create_default_context()

    # Tries to send email - if successful, sends email and stores websites down into notifications table with 'success'
    # for email sent. Otherwise, stores websites as a fail email sent. This helps keep track of notifications that
    # fail for whatever reason.
    try:
        with smtplib.SMTP_SSL(smtpServer, port, context=context) as server:
                server.login(username, password)
                server.sendmail(sender, recipient, msg.as_string())
                db.addNotification(str(downSites), 'success')
    except:
        db.addNotification(str(downSites), 'fail')
