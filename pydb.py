import _mysql
db=_mysql.connect(host="localhost", user="uptime",
                  passwd="password123!", db="uptime")

db.query("""INSERT INTO outages (sitesAffected, numberOfSites) values ('easyprogramming',1)""")

db.query("""Select * from outages""")

r = db.store_result()
data = r.fetch_row(0,1)
for row in data:
        print(row)
