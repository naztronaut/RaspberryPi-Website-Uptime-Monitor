from crontab import CronTab
import db

user_cron = CronTab(user='pi')


def listCron():
    for job in user_cron:
        print(job)


def updateCheckFrequency(comment, freq, enabled):
    for job in user_cron:
        if job.comment == comment:
            job.minute.every(freq)
            if enabled == '1':
                job.enable()
            else:
                job.enable(False)
            user_cron.write()
            print(comment + " cron job updated successfully. It will now run every " + str(freq) + " minutes")


def updateCron(comment, val, enabled):
    for job in user_cron:
        if job.comment == comment:
            job.setall(val)
            if enabled == '1':
                job.enable()
            else:
                job.enable(False)
            user_cron.write()
            print(comment + " cron job updated successfully. The new cron value is: " + str(val))
