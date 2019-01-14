import MySQLdb
import config.config as config

# db = MySQLdb.connect("localhost","uptime","password123!","uptime")
db = MySQLdb.connect(config.DATABASE_CONFIG['host'], config.DATABASE_CONFIG['dbuser'], config.DATABASE_CONFIG['dbpass'],
                     config.DATABASE_CONFIG['dbname'])

cursor = db.cursor()


###########################################################################################
#                                                                                         #
# Begin Activity Queries                                                                  #
#                                                                                         #
###########################################################################################

# Add all activities to `activity` table for historical purposes and reporting
def addActivity(statustype, sites):
    cursor.execute("""INSERT INTO activity (activityType, sitesAffected) VALUES (%s, %s)""", (statustype, sites))
    db.commit()


# Get current status of all sites
def currentStatus(site, status):
    cursor.execute("""INSERT INTO currentStatus (site, status) VALUES (%s,%s)
                        ON DUPLICATE KEY UPDATE status = %s""", (site, status, status))

###########################################################################################
#                                                                                         #
# End Activity Queries                                                                    #
#                                                                                         #
###########################################################################################


###########################################################################################
#                                                                                         #
# Begin Outage Queries                                                                    #
#                                                                                         #
###########################################################################################

# Insert sites into `outages` as an array
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


###########################################################################################
#                                                                                         #
# End Outage Queries                                                                      #
#                                                                                         #
###########################################################################################


###########################################################################################
#                                                                                         #
# Begin LED Queries                                                                       #
#                                                                                         #
###########################################################################################
# LED Table
def changeLedStatus(color, status):
    cursor.execute("""UPDATE ledStatus set status = %s where color = %s""", (status, color))
    db.commit()

###########################################################################################
#                                                                                         #
# End LED Queries                                                                         #
#                                                                                         #
###########################################################################################


###########################################################################################
#                                                                                         #
# Begin Cron Queries                                                                      #
#                                                                                         #
###########################################################################################

# Add new cronjob to database
def addCron(comment, cronName, cronVal, cronScript, enabled):
        cursor.execute("""INSERT INTO cronSettings (comment, cronName, cronVal, cronScript, enabled) 
                        VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE cronName = %s, cronVal = %s, 
                        enabled = %s""", (comment, cronName, cronVal, cronScript, enabled, cronName, cronVal, enabled))
        db.commit()


# Find and update cron job in database
def updateCron(comment, cronVal):
        cursor.execute("""UPDATE cronSettings set cronVal = %s WHERE
                        comment = %s""", (cronVal, comment))
        db.commit()


###########################################################################################
#                                                                                         #
# End Cron Queries                                                                        #
#                                                                                         #
###########################################################################################


###########################################################################################
#                                                                                         #
# Begin Notifications Queries                                                             #
#                                                                                         #
###########################################################################################

def addNotification(text):
    cursor.execute("""INSERT INTO notifications (content) VALUES %s""" % text)
    db.commit()


###########################################################################################
#                                                                                         #
# End Notifications Queries                                                               #
#                                                                                         #
###########################################################################################
