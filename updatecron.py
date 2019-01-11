from crontab import CronTab
import db

user_cron = CronTab(user='pi')


def listCron():
    for job in user_cron:
        print(job)


def findAndUpdate(comment, freq):
    for job in user_cron:
        if job.comment == comment:
            job.minute.every(freq)
            user_cron.write()
            print(comment + " cron job updated successfully. It will now run every " + str(freq) + " minutes")
            db.updateCron(comment, freq)


#findAndUpdate('checkSites', 15)
