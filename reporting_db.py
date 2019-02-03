import MySQLdb
import MySQLdb.cursors
import config.config as config
import json
import datetime


db = MySQLdb.connect(host=config.DATABASE_CONFIG['host'],user=config.DATABASE_CONFIG['dbuser'],
    passwd=config.DATABASE_CONFIG['dbpass'],db=config.DATABASE_CONFIG['dbname'],
    cursorclass=MySQLdb.cursors.DictCursor)

cursor = db.cursor()


# Get Current Status of all sites ever entered into the system
# Columns: id, createdAt, site, status
def getCurrentStatus(page, limit):
    pg = (page - 1) * limit
    cursor.execute("""SELECT * FROM currentStatus LIMIT %s,%s""", (pg, limit))
    data = cursor.fetchall()
    return data


# Get all activity ever recorded. Recorded every 15 minutes by default.
# Columns: id, activityType, createdAt, sitesAffected (returns one site and reports activity type as up or down)
def getActivity(page, limit):
    pg = (page - 1) * limit
    cursor.execute("""SELECT * FROM activity ORDER BY id DESC LIMIT %s,%s""", (pg, limit))
    data = cursor.fetchall()
    return data


# Get all outages reported - multiple sites can be listed
# Columns: id, createdAt, sitesAffected (returns array), numberOfSites
def getOutages(page, limit):
    pg = (page - 1) * limit
    cursor.execute("""SELECT * FROM outages ORDER BY id DESC LIMIT %s,%s""", (pg, limit))
    data = cursor.fetchall()
    return data


# Get downtime counts - the count increases by 1 if site is still down and resets to 0 when site comes back up
# Columns: id, created_at, site, downCount
# Ideally want to archive data from this table at certain points
def getDowntimeCounts(page, limit):
    pg = (page - 1) * limit
    cursor.execute("""SELECT * FROM downtimeCounts LIMIT %s,%s""", (pg, limit))
    data = cursor.fetchall()
    return data


# Get downtime counts if they are greater than 3 because 1 or 2 occurrences can be blips.
def getDownTimeCountsGreaterThanThree():
    cursor.execute("""SELECT * FROM downtimeCounts where downCount >= 3""")
    data = cursor.fetchall()
    return data


# Unused - commenting out for removal later
# def timeConverter(t):
#     if isinstance(t, datetime.datetime):
#         return t.__str__()


# Get LED status for each LED. Can be used later to indicate uptime status on screen instead of lights
# Columns: id, color, pin, updateDate, status
def getLedStatus(color):
    cursor.execute("""SELECT status FROM ledStatus where color = %s""", [color])
    data = cursor.fetchone()
    return data['status']


# Gets cron jobs as defined in the database and whether or not they are enabled
# Columns: id, comment, updateDate, cronName, cronVal, cronScript, enabled
def getCronSettings():
    cursor.execute("""SELECT * FROM cronSettings""")
    data = cursor.fetchall()
    return data


# Get single cron to view and update
def getOneCron(comment):
    cursor.execute("""SELECT * FROM cronSettings where comment = %s""", [comment])
    data = cursor.fetchone()
    return data


# Get all email notifications that were triggered along with if they were successful or fail
# Columns: id, createdAt, content, status - content lists the sites in an array
def getNotifications(page, limit):
    pg = (page - 1) * limit
    cursor.execute("""SELECT * from notifications ORDER BY id DESC LIMIT %s, %s""", (pg, limit))
    data = cursor.fetchall()
    return data
