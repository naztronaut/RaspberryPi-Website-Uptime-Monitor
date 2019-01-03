from crontab import CronTab

user_cron = CronTab(user='pi')


def listCron():
    for job in user_cron:
        print(job)


def cronCheckSites():
    job = user_cron.new(command='cd /home/pi/uptime; /home/pi/uptime/venv/bin/python3 /home/pi/uptime/checkSitesCron.py', comment='checksites')
    job.minute.every(10)
    user_cron.write()


def findCron(comment):
    for job in user_cron:
        if job.comment == comment:
            print(job.comment)
            print(job.command)
            print(job.frequency)
    # print(iter.command)

# listCron()


findCron('checksites')
