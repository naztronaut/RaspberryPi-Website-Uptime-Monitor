import MySQLdb
import MySQLdb.cursors
import config.config as config

# db = MySQLdb.connect("localhost","uptime","password123!","uptime")
db = MySQLdb.connect(config.DATABASE_CONFIG['host'], config.DATABASE_CONFIG['dbuser'], config.DATABASE_CONFIG['dbpass'],
                     config.DATABASE_CONFIG['dbname'],
                     cursorclass=MySQLdb.cursors.DictCursor)

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


# Add site into sites table -  newer than currentStatus
def addSite(name, url, status, active, email, visible):
    cursor.execute("""INSERT INTO sites (siteName, url, status, active, email, visible) 
                            VALUES (%s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE siteName = %s, url = %s, status = %s, 
                            active = %s, email = %s, visible = %s""",
                   (name, url, status, active, email, visible, name, url, status, active, email, visible))
    db.commit()
    cursor.execute("""SELECT * FROM sites where url = %s""", [url])
    data = cursor.fetchone()
    return data


# Update sites and return site after edit
def updateSite(id, name, url, active, email, visible):
    cursor.execute("""UPDATE sites SET siteName = %s, url = %s,
                            active = %s, email = %s, visible = %s WHERE id = %s""",
                   (name, url, active, email, visible, id))
    db.commit()
    cursor.execute("""SELECT * FROM sites where id = %s""", [id])
    data = cursor.fetchone()
    return data


# Update status of site if it's down
def updateSiteStatus(id, status):
    cursor.execute("""UPDATE sites SET status = %s WHERE id = %s""",
                   (status, id))
    db.commit()


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
    cursor.execute("""UPDATE ledStatus set status = %s where pin = %s""", (status, color))
    db.commit()


# Override led
def overrideLedActive(color, active):
    cursor.execute("""UPDATE ledStatus set active = %s where color = %s""", (active, color))
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
def updateCron(comment, cronName, cronVal, enabled):
        cursor.execute("""UPDATE cronSettings set cronName = %s, cronVal = %s, enabled = %s WHERE
                        comment = %s""", (cronName, cronVal, enabled, comment))
        db.commit()
        cursor.execute("""SELECT * FROM cronSettings where comment = %s""", [comment])
        data = cursor.fetchone()
        return data

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

def addNotification(content, status):
    cursor.execute("""INSERT INTO notifications (content, status) values (%s,%s)""", (content, status))
    db.commit()


###########################################################################################
#                                                                                         #
# End Notifications Queries                                                               #
#                                                                                         #
###########################################################################################


###########################################################################################
#                                                                                         #
# Begin archiving queries                                                                 #
#                                                                                         #
###########################################################################################

# Archive records from downtime counts when records are more than 3 days old

def archiveDowntimeCounts():
    cursor.execute("""INSERT INTO archive_downtimeCounts (created_at, site, downCount) 
                    (SELECT created_at,site,downCount FROM downtimeCounts where created_at < (CURDATE() - 3))""")
    db.commit()

    cursor.execute("""DELETE FROM downtimeCounts where created_at < (CURDATE() - 3))""")
    db.commit()


###########################################################################################
#                                                                                         #
# End archiving queries                                                                   #
#                                                                                         #
###########################################################################################
