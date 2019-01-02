import db
import uptime
from crontab import CronTab

user_cron = CronTab('pi')
job = user_cron.new(command='/usr/bin/echo')

job.minute.every(10)
job.enable()
job.write()

# uptime.sites()
