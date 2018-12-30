from flask import Flask, jsonify
import subprocess
import uptime
import json


app = Flask(__name__)


@app.route('/', methods=['GET'])
def getJson():
        print(uptime.sites())
        data = json.loads(uptime.sites())
        return data

