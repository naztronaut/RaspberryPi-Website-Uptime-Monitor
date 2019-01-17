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
            print(enabled)
            if enabled == 1:
                job.enable()
                print('enabled')
            else:
                job.enable(False)
                print('disabled')
            user_cron.write()
            print(comment + " cron job updated successfully. It will now run every " + str(freq) + " minutes")


def updateCron(comment, val, enabled):
    for job in user_cron:
        if job.comment == comment:
            job.setall(val)
            if enabled == 1:
                job.enable()
            else:
                job.enable(False)
            user_cron.write()
            print(comment + " cron job updated successfully. It will now run every " + str(val))
