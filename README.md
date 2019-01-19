# Nazberry Pi - Website Uptime Monitor

**Note: This project is still a work in progress.**

The device monitors a list of your websites and lets you know if any of them are down. Still working on the logic but all green means all good. Red means 3+ sites are down, and yellow means 1-2 are down. More than one light can be on at once for now while I'm still figuring out the logic I want to implement.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

Demo Pic of project in progress:

<img src="https://i.imgur.com/yYHUCZ2.jpg" alt="Website Uptime Monitor" width="700" />

### Hardware

- Raspberry Pi - I use Zero W for this project
- Red Dome LED + Resistor
- Yellow Dome LED + Resistor
- Green Dome LED + Resistor
- Optional protoboard and pins to make a hat for the Pi


### RPi pin usage

The following pin settings were used for this project:

```python
green = 12
yellow = 25
red = 18
```

The pins can be modified in the [LED Pins Configuration](#led-pins) section below

## Installation
The following commands is a rough draft of what needs to be done to install all dependencies.

If you haven't already, You can either clone this repository or download the latest release. To clone the repo run this command:
```bash
git clone https://github.com/naztronaut/RaspberryPi-Website-Uptime-Monitor.git
```

To get the latest release, check out the Latest Releases: https://github.com/naztronaut/RaspberryPi-Website-Uptime-Monitor/releases/latest

At the time of this update, the latest version is version `Beta 0.2.5-b01`. To get this directly, run the following commands:

```bash
wget https://github.com/naztronaut/RaspberryPi-Website-Uptime-Monitor/archive/0.2.5-b01.zip
```

Then unzip it with:

```bash
unzip 0.2.3-alpha.zip
```

For simplicity's sake, I recommend changing the name of the directory/repo to `uptime` as I've done it in and will be using for the rest of this guide. You can do so easily with this command:

```bash
mv RaspberryPi-Website-Uptime-Monitor-0.2.3-alpha uptime
```

Update the directory name as needed. 

### Website List (up.json)

After you clone the repo, you'll see a file called `sites.example.txt` in the folder. This is an example list of sites that I'm monitoring. Rename this to `sites.txt` and add one site per line. 

At this moment, the monitor checks to see if the link location has a `.json` file with the property `site` - this property must be the same URL at which this file is located. Please see the `up.json` file as an example. The content of the file is as follows:

```json
{
  "site": "https://www.easyprogramming.net/up.json"
}
```

If you go to the above  URL, you will find that JSON file with that properly. You don't have to call it `up.json` but for the time being, the location of the file and the property within it must be the same. This is how the script validates that the website is actually loading content and not just returning a status 200.

Avoid having a blank line in your `sites.txt` file. I may put all of this in database tables at some point in the future.  

### Configuration

The below configurations are located in `config/config.sample.py` - before continuing, rename the file to `config.py` and adjust the values below. There are two main configuration categorie: Database and Email. 

To rename the file, run this command:

```bash
mv config.sample.py config.py
```

### LED Pins

The GPIO pins for the LEDs that you will install can be modified in the conf file. Edit the `LED_PINS` object as you see fit. By default, the pins listed above are used:

```python
LED_PINS = {
    'green':    12,
    'yellow':   25,
    'red':      18
}
```

### Email Config

If you want to use the email functionality, edit the `EMAIL_CONFIG` object in `config.py` and enter your username and password. The Mail server and Port are also configurable. 
By default, this app uses Gmail as the mail server and port 465 for SSL. Feel free to change the values to your own specs. Recommended to keep port as the SSL port. And finally, 
edit the sender with your email address and recipient as whoever wants to receive the notification. This app currently only allows one recipient. 

```python
EMAIL_CONFIG = {
    'username': '<USERNAME>',
    'password': '<PASSWORD>',
    'smtpServer': 'smtp.gmail.com',
    'port': 465,
    'sender': 'Email of who will send it',
    'recipient': 'Email of who will receive it'
}
```  

Once you've made the edits, move onto the database config. 

## Database Config

Before creating the schema, edit `config/config.py` and update the `DATABASE_CONFIG` configurations with the database that you'll create in the next step:

```python
DATABASE_CONFIG = {
    'host' : 'localhost',
    'dbname' : 'uptime',
    'dbuser' : 'DATABASE_USER',
    'dbpass' : 'DATABASE_PASSWORD'
}
```

By default, the database name is `uptime` - if you want to use another name, change it. Update the `dbuser` and `dbpass` properties with the credentials that the database will use.

If you change the database name, make sure to edit schema.sql with `nano schema.sql` and update the name in the first two lines:

```sql
CREATE DATABASE `uptime`;
USE `uptime`;
```

The Schema also includes a `ledStatus` table that stores the current status of the LEDs. The default pins listed above are used. If you are using other GPIO Pins, 
please update the `INSERT` query on line 61 to the GPIO Pin Id that you are using:

```sql
INSERT INTO ledStatus (color, pin, status) VALUES ('red', 18, 0),('yellow',25,0),('green',12,0);
```

The above table is used for turning off the Green LED during off hours using cron jobs explained below. 

Now you can run the schema.sql with the following command:
```bash
source database/schema.sql
```

### Virtual Environment & Dependencies

In the main repo directory, install a virtual environment:
```bash
python3 -m venv venv
```

Activate the virtual environment:
```bash
. venv/bin/activate
```

Let's install five more dependencies. Installing flask right away isn't necessary unless you want a UI for your web service:
```bash
pip install RPi.GPIO flask mysqlclient requests python-crontab
```

## Initialize Cron jobs

This app runs automatically via cron jobs. You can initialize some Cron Jobs that are put in place. Before proceeding, edit the `initCron.py` file and edit the two instances of the directory called `uptime` on 
line 17 to whatever you called your repository.

After making the edit, run the script with the following command:

```bash
python3 initCron.py
```

This script will add the cron jobs listed below to crontab as well as to the `cronSettings` MySQL table. Running `initCron.py` will clear your crontab and rewrite all defaults.

Current Cronjobs:

- **Check Sites** - by default, this will check sites every 15 minutes to see if they are online
- **Enable/Disable Green LED** - by default, the Green LED will be turned off between 12:30 AM and 5:30 PM on weekdays and 1 am and 8 am on weekends. 
This is the assumption that you will not be home to see the light. This will NOT affect the red and yellow lights. You can change the values in the init file or later in the crontab. 
- **Email Notification** - a cron will run 1 minute after the sites are checked to get a count of how many times a particular site has been down. If a site has been reported down 3 times in a row, 
it will trigger an email from the sender to recipient email address as specified in `config.py`.

If you want to add or update your cron after you've run `initCron.py`, you can easily edit the official crontab with the following command:

```bash
crontab -e
```

You can also update the database manually. You can also edit the `initCron.py` file and add a new method or edit an old one with your Cron settings and re-run the `initCron.py` script. 
I will add a way to programmatically update your settings in the future.  

## Flask

Web service end points have been created with Flask that can be connected to via a frontend web application or a simple Post request. The end points are still being built. The information below will help you get 
the flask app started as well as understand some of the basic endpoints. Most end points return JSON, some may return basic text. More details below. 

### Run Flask APP

**Note:** _The flask app is still under construction. So far, a few web service end points have been created. More will be added._  

Running a flask app is fairly simple. The controller for the Flask app is `upService.py`. Once you have flask installed in your virtual environment, you can start flask with the following commands:

```bash
export FLASK_APP=upService.py
```

Then run the actual flask app:

```bash
flask run --host=0.0.0.0
```

You can now access it from any computer on your network (assuming there are no firewall settings blocking this) by going to http://ip_addr:5000 - 
substitute `ip_addr` for the IP address for your pi. Hostname will also work in some instances depending on your network setup.

Details on the Flask app will be posted later. 

### Web Service Endpoints

Note: All `GET` requests below have two URL parameters that they accept. They are `page` with a default value of 1 and `limit` with a default value of 25. 

#### 1. Update Status

You can run the website checks manually with `/updateStatus` - it may take a few seconds to a minute to return something depends on how many sites are being checked.

#### 2. GET Current Status

You can get the current status of all websites checked with this end point: `/getCurrentStatus` 

Sites previously checked but removed from the list will return as `down`. 

#### 2. GET Current Status

You can get the current status of all websites checked with this end point: `/getCurrentStatus` 

Sites previously checked but removed from the list will return as `down`. 

#### 3. GET Activity

Every time the `uptime.py` script is run, it's recorded in the database. The `/getActivity` end point will grab you every entry. Note that this list can get very long.  

#### 4. Other GET requests (will be documented later)

1. `/getOutages`
2. `/getDowntimeCounts`
3. `/getCron/`
4. `/getNotifications`

#### POST and PUT requests

1. `/overrideGreen` - override the database value that keeps the green light turned off. `PUT` request taking one parameter: `status` (0 or 1)
2. `/checkFrequency` - Changes the frequency at which the regular site check runs. By default it's every 15 minutes. `PUT` request that takes three parameters: `cronName`, `cronVal`, and `enabled` (0 or 1)
3. `/updateCron` - Changes the crontab values of placed cronjobs based on comment name. `PUT` request that takes 4 paramters: `comment` (unique identifier), `cronName`, `cronVal`, and `enabled` (0 or 1).

More will be added. Want me to add something specific, let me know!

## Backlog items:

1. Web service access (currently in progress as a Flask app)
2. Database integration - for reporting purposes (COMPLETE)
3. Cron Jobs (COMPLETE)
4. Ability to add and update cron jobs programmatically (partially complete)
5. Notification via email (Mostly Complete) 
6. Front-End UI (not started - Planning on creating a separate Angular app that consumes the Flask Web Service endpoints) 
 
Want to add an item to the backlog? Submit an issue. 

## Authors

* **Nazmus Nasir** - [Easy Programming](https://www.easyprogramming.net)


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
