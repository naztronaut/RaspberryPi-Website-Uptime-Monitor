import db
from crontab import CronTab

user_cron = CronTab(user='pi')

cronList = [
    {
        'comment': 'checkSites',
        'name': 'Check Sites',
        'cronScript': 'checkSitesCron',
        'frequency': '10'
    }
]


def cronCheckSites():
    for item in cronList:
        job = user_cron.new(command='cd /home/pi/uptime; /home/pi/uptime/venv/bin/python3 /home/pi/uptime/' +
                            item['cronScript'] + '.py', comment=item['comment'])
        job.minute.every(item['frequency'])
        user_cron.write()
        db.addCron(item['comment'], item['name'], item['frequency'], item['cronScript'], 1)
        print('Successfully added job titled ' + item['name'] + ' with comment #' + item['comment'])


def cronGreenLedOff():
    job = user_cron.new(command='cd /home/pi/uptime; /home/pi/uptime/venv/bin/python3 /home/pi/uptime/cronGreenLed.py LOW', comment='greenLedOff')
    job.setall('0 0 * * 0,1,2,3,4,5,6')
    user_cron.write()
    db.addCron('greenLedOff', 'Green LED Off', '0 0 * * 0,1,2,3,4,5,6', 'cronGreenLed.py', 1)

def cronGreenLedOn():
    job = user_cron.new(command='cd /home/pi/uptime; /home/pi/uptime/venv/bin/python3 /home/pi/uptime/cronGreenLed.py HIGH', comment='greenLedOn')
    job.setall('30 17 * * 0,1,2,3,4,5,6')
    user_cron.write()
    db.addCron('greenLedOn', 'Green LED On', '30 17 * * 0,1,2,3,4,5,6', 'cronGreenLed.py', 1)

cronCheckSites()
cronGreenLedOff()
cronGreenLedOn()
