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