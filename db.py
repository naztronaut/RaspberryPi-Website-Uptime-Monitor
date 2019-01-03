import MySQLdb
import database.config as config

# db = MySQLdb.connect("localhost","uptime","password123!","uptime")
db = MySQLdb.connect(config.DATABASE_CONFIG['host'], config.DATABASE_CONFIG['dbuser'], config.DATABASE_CONFIG['dbpass'],
                     config.DATABASE_CONFIG['dbname'])

cursor = db.cursor()


# cursor.execute("""SELECT * FROM outages""")
# r = db.store_result()
# data = cursor.fetchall()
# for row in data:
#        print(row)

def currentStatus(site, status):
    cursor.execute("""INSERT INTO currentStatus (site, status) VALUES (%s,%s)
                        ON DUPLICATE KEY UPDATE status = %s""", (site, status, status))


# Insert sites innto `outages` as an array
def insertSites(sites, numSites):
    cursor.execute("""INSERT INTO outages (sitesAffected, numberOfSites) values (%s,%s)""", (sites, numSites))
    db.commit()


# Insert sites that are offline to `downtimeCounts` - if they already exist, increase the downCount by 1
# Should trigger an email after 3
def insertDownSite(site):
    cursor.execute("""INSERT INTO downtimeCounts (site, downCount) VALUES(%s, 1)
                        ON DUPLICATE KEY UPDATE downCount=downCount+1""", [site])
    db.commit()


# first checks to see if site exists in the `downtimeCounts` table -
# only triggered if site is found in the uptime array in uptime.py
# if entry exists, set the downCount to 0
# table should be truncated overnight (need to implement archive table)
def checkSite(site):
    data = cursor.execute("""SELECT 1 FROM downtimeCounts where site = %s""", [site])
    # print(data)
    if data >= 1:
        cursor.execute("""UPDATE downtimeCounts set downCount = 0 where site = %s""", [site])
        # print(site + " is back up!")
    db.commit()


# Add all activities to `activity` table for historical purposes and reporting
def addActivity(statustype, sites):
    cursor.execute("""INSERT INTO activity (activityType, sitesAffected) VALUES (%s, %s)""", (statustype, sites))
    db.commit()


# Cron settings
def addCron(cronName, cronVal, cronScript, enabled):
        cursor.execute("""INSERT INTO cronSettings (cronName, cronVal, cronScript, enabled) VALUES (%s, %s, %s, %s)""",
                       (cronName, cronVal, cronScript, enabled))
        db.commit()


def updateCron(cronName, cronVal, cronScript, enabled):
        cursor.execute("""UPDATE cronSettings set cronName = %s, cronVal = %s, cronScript = %s, enabled = %s)""",
                       (cronName, cronVal, cronScript, enabled))
        db.commit()
