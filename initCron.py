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


cronCheckSites()
