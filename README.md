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

## Installation
The following commands is a rough draft of what needs to be done to install all dependencies.

If you haven't already, first clone this repository:
```bash
git clone https://github.com/naztronaut/RaspberryPi-Website-Uptime-Monitor.git
```

For simplicity's sake, I recommend changing the name of the directory/repo to `uptime` as I've done it in and will be using for the rest of this guide. You can do so easily with this command:

```bash
mv RaspberryPi-Website-Uptime-Monitor uptime
```

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

### Email Config

If you want to use the email functionality, edit the `EMAIL_CONFIG` object in `config.py` and enter your username and password. The Mail server and Port are also configurable. 
By default, this app uses Gmail as the mail server and port 465 for SSL. Feel free to change the values to your own specs. Recommended to keep port as the SSL port. 

```python
EMAIL_CONFIG = {
    'username': '<USERNAME>',
    'password': '<PASSWORD>',
    'smtpServer': 'smtp.gmail.com',
    'port': 465
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

This script will add the cron jobs listed below to crontab as well as to the cronSettings MySQL table:

- Check Sites - by default, this will check sites every 15 minutes to see if they are online
- Turn Off Green LED - by default, the Green LED will be turned off between 12:30 AM and 5:30 PM on weekdays and 1 am and 8 am on weekends. 
This is the assumption that you will not be home to see the light. This will NOT affect the red and yellow lights. You can change the values in the init file or later in the crontab. 
- Emails - a cron will run 1 minute after the sites are checked to get a count of how many times a particular site has been down. If a site has been reported down 3 times in a row, it will trigger an email.

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

## Backlog items:

1. Web service access (currently in process as a Flask app)
2. Database integration - for reporting purposes (in progress)
3. Cron Jobs (in progress)
4. Notification via email 
 

## Authors

* **Nazmus Nasir** - [Easy Programming](https://www.easyprogramming.net)


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
