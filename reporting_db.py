import MySQLdb
import MySQLdb.cursors
import database.config as config
import json
import datetime


db = MySQLdb.connect(host=config.DATABASE_CONFIG['host'],user=config.DATABASE_CONFIG['dbuser'],
    passwd=config.DATABASE_CONFIG['dbpass'],db=config.DATABASE_CONFIG['dbname'],
    cursorclass=MySQLdb.cursors.DictCursor)

cursor = db.cursor()


def getCurrentStatus(page, limit):
    pg = (page - 1) * limit
    cursor.execute("""SELECT * FROM currentStatus LIMIT %s,%s""", (pg, limit))
    data = cursor.fetchall()
    return data


def getActivity(page, limit):
    pg = (page - 1) * limit
    cursor.execute("""SELECT * FROM activity LIMIT %s,%s""", (pg, limit))
    data = cursor.fetchall()
    return data


def getOutages(page, limit):
    pg = (page - 1) * limit
    cursor.execute("""SELECT * FROM outages LIMIT %s,%s""", (pg, limit))
    data = cursor.fetchall()
    return data


def getDowntimeCounts(page, limit):
    pg = (page - 1) * limit
    cursor.execute("""SELECT * FROM downtimeCounts LIMIT %s,%s""", (pg, limit))
    data = cursor.fetchall()
    return data


def timeConverter(t):
    if isinstance(t, datetime.datetime):
        return t.__str__()


def getLedStatus(color):
    cursor.execute("""SELECT status FROM ledStatus where color = %s""", [color])
    data = cursor.fetchone()
    return data


getLedStatus('green')
