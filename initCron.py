import db
from crontab import CronTab

user_cron = CronTab(user='pi')

# Clear all crons to set everything back to default
user_cron.remove_all()
user_cron.write()

cronList = [
    {
        'comment': 'checkSites',
        'name': 'Check Sites',
        'cronScript': 'checkSitesCron',
        'frequency': '15'
    }
]


# Check sites cron every 10 minutes
def cronCheckSites():
    for item in cronList:
        job = user_cron.new(command='cd /home/pi/uptime; /home/pi/uptime/venv/bin/python3 /home/pi/uptime/' +
                            item['cronScript'] + '.py', comment=item['comment'])
        job.minute.every(item['frequency'])
        user_cron.write()
        db.addCron(item['comment'], item['name'], item['frequency'], item['cronScript'], 1)
        print('Successfully added job titled ' + item['name'] + ' with comment #' + item['comment'])


# Allow green light to be turned on after 5:30 pm tuesday through friday
def cronGreenLedOn():
    job = user_cron.new(command='cd /home/pi/uptime; /home/pi/uptime/venv/bin/python3 /home/pi/uptime/cronGreenLed.py '
                                'HIGH', comment='greenLedOn')
    job.setall('30 17 * * 2,3,4,5')
    user_cron.write()
    db.addCron('greenLedOn', 'Green LED On Weekday', '30 17 * * 2,3,4,5', 'cronGreenLed.py', 1)


# Make sure green light is turned off after midnight tuesday through friday
def cronGreenLedOff():
    job = user_cron.new(command='cd /home/pi/uptime; /home/pi/uptime/venv/bin/python3 /home/pi/uptime/cronGreenLed.py '
                                'LOW', comment='greenLedOff')
    job.setall('0 0 * * 2,3,4,5')
    user_cron.write()
    db.addCron('greenLedOff', 'Green LED Off Weekday', '0 0 * * 2,3,4,5', 'cronGreenLed.py', 1)


# Allow green light to be on after 8 am on weekends (and Monday)
def cronGreenLedWeekendOn():
    job = user_cron.new(command='cd /home/pi/uptime; /home/pi/uptime/venv/bin/python3 /home/pi/uptime/cronGreenLed.py '
                                'HIGH', comment='greenLedOnWeekend')
    job.setall('0 8 * * 0,1,6')
    user_cron.write()
    db.addCron('greenLedOnWeekend', 'Green LED On Weekend', '0 8 * * 0,1,6', 'cronGreenLed.py', 1)


# Turn off green light on weekends after 1 am (and Monday)
def cronGreenLedWeekendOff():
    job = user_cron.new(command='cd /home/pi/uptime; /home/pi/uptime/venv/bin/python3 /home/pi/uptime/cronGreenLed.py '
                                'LOW', comment='greenLedOffWeekend')
    job.setall('0 1 * * 0,1,6')
    user_cron.write()
    db.addCron('greenLedOffWeekend', 'Green LED Off Weekend', '0 1 * * 0,1,6', 'cronGreenLed.py', 1)


# Send out notifications via email every 1, 16, 31, and 46 minutes every hour.
# Gives 1 minute between checking websites and sending notifications
def cronOutageEmail():
    job = user_cron.new(command='cd /home/pi/uptime; /home/pi/uptime/venv/bin/python3 /home/pi/uptime/cronOutage.py',
                        comment='emailNotification')
    job.setall('1-46/15 * * * *')
    user_cron.write()
    db.addCron('outageEmail', 'Outage Email', '1-46/15 * * * *', 'cronGreenLed.py', 1)


cronCheckSites()
cronGreenLedOn()
cronGreenLedOff()
cronGreenLedWeekendOn()
cronGreenLedWeekendOff()
cronOutageEmail()
