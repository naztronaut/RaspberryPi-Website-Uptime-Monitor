import reporting_db as rdb
import outageEmail as oe

data = rdb.getDownTimeCountsGreaterThanThree()

downSites = []
count = 0

for item in data:
    print(item)
    if item['downCount'] >= 3:
        count += 1
        downSites.append(item['site'])

oe.outage(downSites, count)
