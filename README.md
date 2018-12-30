# Nazberry Pi - Website Uptime Monitor

**Note: This project is still a work in progress.**

The device monitors a list of your websites and lets you know if any of them are down. Still working on the logic but all green means all good. Red means 3+ sites are down, and yellow means 1-2 are down. More than one light can be on at once for now while I'm still figuring out the logic I want to implement.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Hardware

Raspberry Pi - I use Zero W for this project

### RPi pin usage

The followig pin settings were used for this project

```python
green = 12
yellow = 25
red = 18
```

## Installation
The following commands is a rough draft of what nees to be done to install all dependencies. Details will be posted later:

If you haven't already, first clone this repository:
```
git clone https://github.com/naztronaut/RaspberryPi-Website-Uptime-Monitor.git
```

Once you've cloned it, `cd` into the directory and install a virtual environment:
```
python3 -m venv venv
```

Activate the virtual environment:
```
. venv/bin/activate
```

Let's install four more dependencies. Installing flask right away isn't necessary unless you want a UI for your web service:
```
pip install RPi.GPIO flask mysqlclient requests
```

### Run Flask APP
Running a flask app is fairly simple. Once you have flask installed in your virtual environment, let's run this command:
```
export FLASK_APP=upService.py
```

Then when we are done, let's run the actual flask app:
```
flask run --host=0.0.0.0
```

You can now access it from any computer on your network (assuming there are no firewall settings blocking this) by going to http://ip_addr:5000 - substitude ip_addr for the IP address for your pi. Hostname will also work in some instances.

## Backlog items:

1. Web service access (currently in process as a Flask app)
2. Database integration - for reporting purposes
3. Notification via email 
 

## Authors

* **Nazmus Nasir** - [Easy Programming](https://www.easyprogramming.net)


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
