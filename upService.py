from flask import Flask, jsonify, request
import subprocess
import uptime
import json
import reporting_db as db


app = Flask(__name__)


@app.route('/', methods=['GET'])
def homePage():
	return "There's nothing here. Find your own way!"


# Manually updates all statuses and updates the database
@app.route('/updateStatus', methods=['GET'])
def getJson():
        #print(uptime.sites())
        data = json.loads(uptime.sites())
        return data


@app.route('/getCurrentStatus', methods=['GET'])
def getCurrentStatus():
	page = request.args.get('page',default=1,type=int)
	limit = request.args.get('limit',default=10,type=int)
	data = db.getCurrentStatus(page, limit)
	return jsonify(data)


@app.route('/getActivity', methods=['GET'])
def getActivity():
	page = request.args.get('page',default=1,type=int)
	limit = request.args.get('limit',default=25,type=int)
	data = db.getActivity(page, limit)
	return jsonify(data)

@app.route('/getOutages', methods=['GET'])
def getOutages():
	page = request.args.get('page',default=1,type=int)
	limit = request.args.get('limit',default=25,type=int)
	data = db.getOutages(page, limit)
	return jsonify(data)

@app.route('/getDowntimeCounts', methods=['GET'])
def getDowntimeCounts():
	page = request.args.get('page',default=1,type=int)
	limit = request.args.get('limit',default=25,type=int)
	data = db.getOutages(page, limit)
	return jsonify(data)
