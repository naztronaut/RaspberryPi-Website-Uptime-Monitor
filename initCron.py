import db
from crontab import CronTab

user_cron = CronTab(user='pi')

cronList = [
    {
        'name': 'Check Sites',
        'scriptName': 'checkSitesCron',
        'frequency': '10'
    }
]

def cronCheckSites():
    for item in cronList:
        job = user_cron.new(command='cd /home/pi/uptime; /home/pi/uptime/venv/bin/python3 /home/pi/uptime/' +
                            item.scriptName + '.py', comment='checksites')
        job.minute.every(item.frequency)
        user_cron.write()
        db.addCron(item.scriptName, item.frequency, item.cronScript, 1)
        print('Successfully added job titled ' + item.name)
