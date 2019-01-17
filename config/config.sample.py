# config.sample.py
# Rename this file to config.py before running this application and change the database values below


# LED GPIO Pin numbers - these are the default values, feel free to change them as needed
LED_PINS = {
    'green':    12,
    'yellow':   25,
    'red':      18
}


EMAIL_CONFIG = {
    'username': '<USERNAME>',
    'password': '<PASSWORD>',
    'smtpServer': 'smtp.gmail.com',
    'port': 465,
    'sender': 'Email of who will send it',
    'recipient': 'Email of who will receive it'
}


DATABASE_CONFIG = {
    'host' : 'localhost',
    'dbname' : 'uptime',
    'dbuser' : 'DATABASE_USER',
    'dbpass' : 'DATABASE_PASSWORD'
}
