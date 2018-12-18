import RPi.GPIO as GPIO
# import subprocess
import requests
import json
# import sys

green = 12
yellow = 25
red = 18
# hard coded number of sites
totalSites = 4
global upSites
upSites = []
global downSites
downSites = []


def sites():
    global js
    with open("sites.txt") as f:
        for line in f:
            # print(line)
            # downcount += isItUp(line)
            isItUp(line)
    if len(upSites) + len(downSites) == 4:
        js = '{"up": "' + str(len(upSites)) + '", "down" : "' + str(len(downSites)) + '", "upSites": "' + str(upSites) + '", "downSites": "' + str(downSites) + '"}'

    print(js)
    return json.dumps(js)


def isItUp(site):
    upSites = []
    downSites = []
    site = site.replace('\n', '')

    data = requests.get(site)

    # only proceed if page loads successfully with status code of 200
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
                # print('Site URL different from site url passed')
                downSites.append(site)
                dataOutput(site, 'down')
        except:
            downSites.append(site)
            dataOutput(site, 'down')
    else:
        downSites.append(site)
        dataOutput(site, 'down')


def changeLight(color, status):
    {}
    # if status == "high":
    #     output = GPIO.HIGH
    # else:
    #     output = GPIO.LOW
    #
    # GPIO.setmode(GPIO.BCM)
    # GPIO.setwarnings(False)
    # GPIO.setup(color, GPIO.OUT)
    # GPIO.output(color, output)


def dataOutput(site, status):
    if status == 'up':
        upSites.append(site.replace('\n', ''))
    else:
        downSites.append(site.replace('\n', ''))

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

    if len(upSites) >= 1:
        changeLight(green, 'high')
    else:
        changeLight(green, 'low')


sites()
