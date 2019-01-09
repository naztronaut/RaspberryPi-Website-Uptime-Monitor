# config.sample.py
# Rename this file to config.py before running this application and change the database values below

DATABASE_CONFIG = {
    'host' : 'localhost',
    'dbname' : 'uptime',
    'dbuser' : 'DATABASE_USER',
    'dbpass' : 'DATABASE_PASSWORD'
}

EMAIL_CONFIG = {
    'username': '<USERNAME>',
    'password': '<PASSWORD>',
    'smtpServer': 'smtp.gmail.com',
    'port': 465
}