from crontab import CronTab

user_cron = CronTab(user='pi')

job = user_cron.new(command='python3 checkSitesCron.py', comment='checksites')

job.minute.every(10)
user_cron.write()

