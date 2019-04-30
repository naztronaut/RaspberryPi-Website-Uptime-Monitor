import RPi.GPIO as GPIO
import requests
import json
import db
import reporting_db as rdb
import config.config as config

green = config.LED_PINS['green']
yellow = config.LED_PINS['yellow']
red = config.LED_PINS['red']
global upSites
upSites = []
global downSites
downSites = []


# Main method - reads the list of sites in sites.txt and checks using isItUp() method
def sites():
    global js
    global totalSites
    totalSites = 0
    # gets sites from database now - dependency on up.json was removed
    json_object = (rdb.getSitesForCheck())
    for item in json_object:
        status = isItUp(item['url'])
        try:
            if status == True:
                upSites.append(item['url'])
                dataOutput(item['id'], item['url'], item['siteName'], 'up')
            else:
                downSites.append(item['url'])
                dataOutput(item['id'], item['url'], item['siteName'], 'down')
        except:
            downSites.append(item['url'])
            dataOutput(item['id'], item['url'], item['siteName'], 'down')
    # insert into `outages` table with a list of sites in an array and the length of the downSites arr
    if len(downSites) > 0:
        db.insertSites(str(downSites), str(len(downSites)))
    # trigger updateDownSites() method to store data in `outages` table
    updateDownSites()
    # trigger checkSite() method to trigger double checking of sites that are up
    checkSite()


# Does an HTTP GET on the site URLs being passed and looks for status code 200
# removed dependency on up.json
def isItUp(site):
    try:
        data = requests.get(site)
        if data.status_code == 200:
            return True
        else:
            return False
    except:
        return False


# Outputting data to database tables as well as to lights
def dataOutput(id, siteUrl, siteName, status):
    if status == 'up':
        # upSites.append(site.replace('\n', ''))
        # send to `activity` table as site that is online
        db.addActivity("up", siteName)
        db.currentStatus(siteUrl, "up")
        db.updateSiteStatus(id, "up")
    else:
        # downSites.append(site.replace('\n', ''))
        # send to activity table as site that is offline
        db.addActivity("down", siteName)
        db.currentStatus(siteUrl, "down")
        db.updateSiteStatus(id, "down")
    if len(downSites) >= 3:
        changeLight(red, 'high')
        changeLight(yellow, 'low')
        changeLight(green, 'low')
    elif len(downSites) >= 1:
        changeLight(yellow, 'high')
        changeLight(red, 'low')
    else:
        changeLight(green, 'high')
        changeLight(red, 'low')
        changeLight(yellow, 'low')

    # Checks upsites separately
    # If at least one site is online, green light is on. Indicates that at least the world isn't ending
    if len(upSites) >= 1:
        changeLight(green, 'high')
    else:
        changeLight(green, 'low')


# Changes LED on/off status
def changeLight(color, status):
    # will only turn on green led if it hasn't been turned off by the cron jobs at night
    # red and yellow lights are not affected by those values
    if (color == green and rdb.getLedActive('green') == 1) or color == red or color == yellow:
        if status == "high":
            output = GPIO.HIGH
            db.changeLedStatus(color, 1)
            # Only affect red and yellow lights
            # if color == red:
            #     db.changeLedStatus('red', 1)
            # elif color == yellow:
            #     db.changeLedStatus('yellow', 1)
        else:
            output = GPIO.LOW
            db.changeLedStatus(color, 0)
            # Only affect red and yellow lights
            # if color == red:
            #     db.changeLedStatus('red', 0)
            # elif color == yellow:
            #     db.changeLedStatus('yellow', 0)

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(color, GPIO.OUT)
        GPIO.output(color, output)


# Inserts data into downtimeCounts() table to either add or update the number of times a site has failed to respond
def updateDownSites():
    for site in downSites:
        # insert into `downsitesCount` table and increment downCount by 1 if applicable
        db.insertDownSite(site)


# Check sites in upSites to against the downsiteCounts table to see if a site has come back to life
def checkSite():
    for site in upSites:
        # check the downsiteCount table for all sites in the upSites[] list - 
        # if record exists, then it'll set the downCount to 0
        db.checkSite(site)


# sites()
