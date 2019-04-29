# Raspberry Pi - Website Uptime Monitor

The device monitors a list of your websites and lets you know if any of them are down. Still working on the logic but all green means all good. Red means 3+ sites are down, and yellow means 1-2 are down. More than one light can be on at once for now while I'm still figuring out the logic I want to implement.

## Demo
<a href="https://www.youtube.com/watch?v=CBtRuy5vFhI" target="_blank"><img src="https://www.easyprogramming.net/img/uptimeMonitor.jpg" width="700" /></a>
###### Click image to watch demo on YouTube

## Table of Contents

1. [Getting Started](#getting-started)
    1. [Hardware](#hardware)
    2. [RPi Pin Usage](#rpi-pin-usage)
2. [Installation](#installation)
    1. [Website List](#website-list-upjson)
3. [Configuration](#configuration)
    1. [LED Pins](#led-pins)
    2. [Email Config](#email-config)
    3. [Database Config](#database-config)
    4. [Virtual Environment](#virtual-environment--dependencies)
4. [Cron Jobs](#initialize-cron-jobs)
5. [Flask](#flask)
    1. [Run Flask App](#run-flask-app)
    2. [Web Service Endpoints](#web-service-endpoints)
6. [Apache](#apache)
7. [Backlog Items](#backlog-items)
8. [Authors](#authors)
9. [License](#license)
    

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

**NOTE**: _This guide assumes that you have MySQL installed with a database named `uptime` - you can change the database name and user in the configurations below._  

If you haven't already, You can either clone this repository or download the latest release. To clone the repo run this command:
```bash
git clone https://github.com/naztronaut/RaspberryPi-Website-Uptime-Monitor.git
```

To get the latest release, check out the Latest Releases: https://github.com/naztronaut/RaspberryPi-Website-Uptime-Monitor/releases/latest

At the time of this update, the latest version is version `Beta 0.3.0-b01`. To get this directly, run the following commands:

```bash
wget https://github.com/naztronaut/RaspberryPi-Website-Uptime-Monitor/archive/0.3.0-b01.zip
```

Then unzip it with:

```bash
unzip 0.3.0-b01.zip
```

For simplicity's sake, I recommend changing the name of the directory/repo to `uptime` as I've done it in and will be using for the rest of this guide. You can do so easily with this command:

```bash
mv RaspberryPi-Website-Uptime-Monitor-0.3.0-b01 uptime
```

Update the directory name as needed. 

### Website List in `sites` table

Dependency on `up.json` was removed as of version `0.5.0`. Sites are now stored in the database inside the `sites` table.  

This application will check to see if a `200` is returned from the website and it will only check websites that are currently active and visible (not deleted). 
The previously used `up.json` didn't do too much in addition to checking for a status of `200` so it was removed. I am working on ideas on how to check the actual content
for a better sense of website uptime. 

## Configuration

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

### Database Config

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

Running a flask app is fairly simple. To run apache in front of flask so that you can access your app without needing the port, read the [Apache](#apache) section below. 

The controller for the Flask app is `upService.py`. Once you have flask installed in your virtual environment, you can start flask with the following commands:

```bash
export FLASK_APP=upService.py
```

Then run the actual flask app:

```bash
flask run --host=0.0.0.0
```

You can now access it from any computer on your network (assuming there are no firewall settings blocking this) by going to http://ip_addr:5000 - 
substitute `ip_addr` for the IP address for your pi. Hostname will also work in some instances depending on your network setup. 
The apache section below will cover how to run your flask app through apache.

Details on the Flask app will be posted later. 

### Web Service Endpoints

Note: All `GET` requests below have two URL parameters that they accept. They are `page` with a default value of 1 and `limit` with a default value of 25. 

#### 1. Sites

You can get a list of all sites being monitored with the `/getSites` endpoint. You can add a site with `/addSite` and pass in these items:

- `siteName` - name of the site 
- `url` - url to be monitored
- `email` - email address which will be contacted if the site goes down

New sites are automatically set to the active status, but can be turned off by changing the `active` property to `0`. 

You can update a site by using the `/updateSite` endpoint. Along with the three properties above, send these additional two to update the site:

- `id` - in order to edit a site, it must exist with an unique id in the database
- `active` - change the active status to either 1 (active) or 0 (inactive)

Delete functionality will be coming in a future release. It will be a soft delete (visibility will be set to 0 instead of removing the row from the database). 

#### 2. Update Status

You can run the website checks manually with `/updateStatus` - it may take a few seconds to a minute to return something depends on how many sites are being checked.

#### 3. GET Current Status (Sites component replaces this)

Note: This will eventually be deprecated since the Sites component handles everything here and more. 

You can get the current status of all websites checked with this end point: `/getCurrentStatus` 

Sites previously checked but removed from the list will return as `down`. 

#### 4. GET Activity

Every time the `uptime.py` script is run, it's recorded in the database. The `/getActivity` end point will grab you every entry. Note that this list can get very long.  

#### 5. Other GET requests (will be documented later)

1. `/getOutages`
2. `/getDowntimeCounts`
3. `/getCron/`
4. `/getNotifications`

#### POST and PUT requests

1. `/overrideGreen` - override the database value that keeps the green light turned off. `PUT` request taking one parameter: `status` (0 or 1)
2. `/checkFrequency` - Changes the frequency at which the regular site check runs. By default it's every 15 minutes. `PUT` request that takes three parameters: `cronName`, `cronVal`, and `enabled` (0 or 1)
3. `/updateCron` - Changes the crontab values of placed cronjobs based on comment name. `PUT` request that takes 4 paramters: `comment` (unique identifier), `cronName`, `cronVal`, and `enabled` (0 or 1).
4. '/updateSite' - new - will update sites

More will be added. Want me to add something specific, let me know!

## Apache

### Installation

We need to install Apache2 as well as Libapache WSGI module. To do so, run this command:

```bash
sudo apt install apache2 libapache2-mod-wsgi-py3 -y
```

This will install the required depencencies. 

Move or copy the `activate_this.py` file from the `util/` dir into your venv folder.  You can do so with this command:

```bash
cp util/activate_this.py venv/bin/
``` 

The file will allow Apache to run your this application from from the virtual environment. The file was last copied on January 31, 2019. To look for updates or to get it directly from the source, you can run this command:

```bash
cd venv/bin
wget https://raw.githubusercontent.com/pypa/virtualenv/master/virtualenv_embedded/activate_this.py
```

This will enter your `venv/bin` dir and download the file from the source (source file does not change often). 

We need to add a new configuration file to Apache. To do this run these:

```bash
cd /etc/apache2/sites-available
```

Create a new .conf file:

```bash
sudo nano uptime.conf
```

Enter this new virtual host information in the file and save:
```apacheconf
<VirtualHost *:80>
    ServerName uptimepi
    WSGIDaemonProcess uptime user=pi group=www-data threads=5
    WSGIScriptAlias /uptime /var/www/html/uptime/uptime.wsgi
    <Directory /var/www/html/uptime>
        WSGIProcessGroup uptime
        WSGIScriptReloading On
        WSGIApplicationGroup %{GLOBAL}
        Require all granted
    </Directory>
</VirtualHost>
```

Then we need to activate this new configuration file and disable the default one with these commands:

```bash
sudo a2ensite uptime.conf
sudo a2dissite 000-default.conf
```

You can then restart apache with `sudo service apache2 restart` now.

As the file suggests, we need the `uptime.wsgi` file in the  `/var/www/html/uptime/` directory so that our apache can access it. So let's do these commands:

```bash
cd /var/www/html
sudo mkdir uptime
cd uptime
```

A wsgi file is already provided in the `util/` directory of this repository. You can either create your own or copy the provided file with this command:

```bash
sudo cp /home/pi/uptime/util/uptime.wsgi /var/www/html/uptime/
```

Adjust the directory from `/uptime/` as you need to if you created your own directory. Note that you will need to update line 3 and 8 of `uptime.wsgi` with the correct directory as well. 

Once this is done, restart apache if you haven't already, open a new browser and go to `http://ip_addr/uptime` - if all goes well, the app should load and you no longer 
need to start Flask every time or use the port 5000. You can use any of the routes available to you. 

What are the benefits of running apache in front of your flask app?

When we create our front-end site, we won't have to worry about CORS when requesting data. We can simply add our front-end to another folder in our web server and use this as one big app!

## Backlog items:

For a better list of backlog items, check out the beta project on Github: https://github.com/naztronaut/RaspberryPi-Website-Uptime-Monitor/projects/1

1. Web service access (currently in progress as a Flask app)
2. Database integration - for reporting purposes (COMPLETE)
3. Cron Jobs (COMPLETE)
4. Ability to add and update cron jobs programmatically (partially complete)
5. Notification via email (Mostly Complete) 
6. Front-End UI (in progress - Planning on creating a separate Angular app that consumes the Flask Web Service endpoints) 
 
Want to add an item to the backlog? Submit an issue. 

## Authors

* **Nazmus Nasir** - [Easy Programming](https://www.easyprogramming.net)


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
