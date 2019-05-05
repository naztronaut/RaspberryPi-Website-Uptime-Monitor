from flask import Flask, jsonify, request
import subprocess
import uptime
import json
import db
import reporting_db as rdb
import updatecron as uc


app = Flask(__name__)


@app.route('/', methods=['GET'])
def homePage():
    return "There's nothing here. Find your own way!"


# Manually updates all statuses and updates the database
@app.route('/updateStatus', methods=['GET'])
def getJson():
        data = json.loads(uptime.sites())
        return data


@app.route('/getCurrentStatus', methods=['GET'])
def getCurrentStatus():
    page = request.args.get('page',default=1,type=int)
    limit = request.args.get('limit',default=10,type=int)
    data = rdb.getCurrentStatus(page, limit)
    return jsonify(data)


@app.route('/getSites', methods=['GET'])
def getSites():
    page = request.args.get('page',default=1,type=int)
    limit = request.args.get('limit',default=100,type=int)
    data = rdb.getSites(page, limit)
    return jsonify(data)

@app.route('/addSite', methods=['POST'])
def addSite():
    siteName = request.form['siteName']
    url = request.form['url']
    status = 0  # default is site is offline until checked
    active = 1  # default active
    email = request.form['email']
    visible = 1  # default visible
    try:
        data = db.addSite(siteName, url, status, active, email, visible)
        # obj = {"status": "successfully added site"}
        # return json.dumps(obj)
        return jsonify(data)
    except:
        obj = {"status": "Failed to add site"}
        return json.dumps(obj)

@app.route('/updateSite', methods=['PUT'])
def updateSite():
    id = request.form['id']
    siteName = request.form['siteName']
    url = request.form['url']
    # status = request.form['status'] #  should only be updated by site check
    active = request.form['active']
    email = request.form['email']
    visible = 1  # default visible
    try:
        data = db.updateSite(id, siteName, url, active, email, visible)
        return jsonify(data)
    except:
        obj = {"status": "Failed to update site"}
        return json.dumps(obj)


@app.route('/getActivity', methods=['GET'])
def getActivity():
    page = request.args.get('page',default=1,type=int)
    limit = request.args.get('limit',default=25,type=int)
    data = rdb.getActivity(page, limit)
    return jsonify(data)


@app.route('/getOutages', methods=['GET'])
def getOutages():
    page = request.args.get('page',default=1,type=int)
    limit = request.args.get('limit',default=25,type=int)
    data = rdb.getOutages(page, limit)
    return jsonify(data)


@app.route('/getDowntimeCounts', methods=['GET'])
def getDowntimeCounts():
    page = request.args.get('page',default=1,type=int)
    limit = request.args.get('limit',default=25,type=int)
    data = rdb.getDowntimeCounts(page, limit)
    return jsonify(data)


@app.route('/getCron', methods=['GET'])
def getCron():
    data = rdb.getCronSettings()
    return jsonify(data)


@app.route('/getNotifications', methods=['GET'])
def getNotifications():
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=25, type=int)
    data = rdb.getNotifications(page, limit)
    return jsonify(data)


# define green LED Override via POST
@app.route('/overrideGreen', methods=['PUT'])
def overrideGreen():
    status = request.form['status']
    try:
        db.changeLedStatus('green', status)
        obj = {"status": "successfully changed LED status"}
        return json.dumps(obj)
    except:
        obj = {"status": "Failed to change LED status"}
        return json.dumps(obj)


@app.route('/getLeds', methods=['GET'])
def getLedStatus():
    data = rdb.getLedStatus()
    return jsonify(data)


@app.route('/changeLedActive', methods=['PUT'])
def changeLedActive():
    color = request.form['color']
    active = request.form['active']
    print(color, active)
    data = db.overrideLedActive(color, active)
    return jsonify(data)


# This will only update the checkSites cron since it only accepts the interval at which sites are
# checked unlike the others
@app.route('/checkFrequency', methods=['PUT'])
def checkFrequency():
    # comment = request.form['comment']
    name = request.form['cronName']
    val = request.form['cronVal']
    enabled = request.form['enabled']

    uc.updateCheckFrequency('checkSites', val, enabled)
    data = db.updateCron('checkSites', name, val, enabled)
    return jsonify(data)


@app.route('/updateCron', methods=['POST', 'PUT'])
def updateCron():
    if request.method == 'PUT':
        comment = request.form['comment']
        name = request.form['cronName']
        val = request.form['cronVal']
        enabled = request.form['enabled']

        uc.updateCron(comment, val, enabled)
        data = db.updateCron(comment, name, val, enabled)
        return jsonify(data)
    elif request.method == 'POST':
        return 'POST Method not set'
    else:
        return 'Only accepts PUT or POST'
