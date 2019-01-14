import smtplib, ssl
import config.config as cred

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import db


def outage(sites, downCount):

    # Config values
    username = cred.EMAIL_CONFIG['username']
    password = cred.EMAIL_CONFIG['password']
    port = cred.EMAIL_CONFIG['port']
    smtpServer = cred.EMAIL_CONFIG['smtpServer']
    sender = cred.EMAIL_CONFIG['sender']
    recipient = cred.EMAIL_CONFIG['recipient']

    dbSites = []

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
        dbSites.append(site['site'])
    html += "</ul>"

    emailMsg = MIMEText(html, "html")

    msg.attach(emailMsg)

    # Add to database - to fix later, currently cannot hold html
    # print(str(dbSites))
    # db.addNotification(str(dbSites))

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(smtpServer, port, context=context) as server:
                server.login(username, password)
                server.sendmail(sender, recipient, msg.as_string())
                db.addNotification(str(dbSites), 'success')
    except:
        db.addNotification(dbSites, 'fail')
