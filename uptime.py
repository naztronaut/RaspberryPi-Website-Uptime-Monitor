import RPi.GPIO as GPIO
import requests
import json
import db
import reporting_db as rdb

green = 12
yellow = 25
red = 18
# hard coded number of sites
global upSites
upSites = []
global downSites
downSites = []


def sites():
    global js
    global totalSites
    totalSites = 0
    # Read list of sites in sites.txt - one site per line
    # make sure the up.json file exists with the property "site"
    with open("sites.txt") as f:
        for line in f:
            totalSites = totalSites + 1
            isItUp(line)

    if len(upSites) + len(downSites) == totalSites:
        js = '{"up": "' + str(len(upSites)) + '", "down" : "' + str(len(downSites)) + '", "upSites": "' + str(
            upSites) + '", "downSites": "' + str(downSites) + '"}'
    # insert into `outages` table with a list of sites in an array and the length of the downSites arr
    if len(downSites) > 0:
        db.insertSites(str(downSites), str(len(downSites)))
    # trigger updateDownSites() method to store data in `outages` table
    updateDownSites()
    # trigger checkSite() method to trigger double checking of sites that are up
    checkSite()
    return json.dumps(js)


def updateDownSites():
    for site in downSites:
        # insert into `downsitesCount` table and increment downCount by 1 if applicable
        db.insertDownSite(site)


def checkSite():
    for site in upSites:
        # check the downsiteCount table for all sites in the upSites[] list - 
        # if record exists, then it'll set the downCount to 0
        db.checkSite(site)


def isItUp(site):
    upSites = []
    downSites = []
    site = site.replace('\n', '')

    # only proceed if page loads successfully with status code of 200
    try:
        data = requests.get(site)
        if data.status_code == 200:
            resp = data.text
            parsed = json.loads(resp)
            # if siteUrl property matches the site url passed, then it'll return a 1, otherwise the page gets a 200 but
            # for some reason, the json file isn't being read
            try:
                if parsed['site'] == site:
                    upSites.append(site)
                    dataOutput(site, 'up')
                else:
                    downSites.append(site)
                    dataOutput(site, 'down')
            except:
                downSites.append(site)
                dataOutput(site, 'down')
        else:
            downSites.append(site)
            dataOutput(site, 'down')
    except:
        downSites.append(site)
        dataOutput(site, 'down')


def changeLight(color, status):
    # will only turn on green led if it hasn't been turned off by the cron jobs at night
    # red and yellow lights are not affected by those values
    if (color == green and rdb.getLedStatus('green') == 1) or color == red or color == yellow:
        if status == "high":
            output = GPIO.HIGH
        else:
            output = GPIO.LOW

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(color, GPIO.OUT)
        GPIO.output(color, output)


def dataOutput(site, status):
    if status == 'up':
        upSites.append(site.replace('\n', ''))
        # send to `activity` table as site that is online
        db.addActivity("up", site)
        db.currentStatus(site, "up")
    else:
        downSites.append(site.replace('\n', ''))
        # send to activity table as site that is offline
        db.addActivity("down", site)
        db.currentStatus(site, "down")
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

#sites()
