import reporting_db as rdb
import outageEmail as oe

data = rdb.getDownTimeCountsGreaterThanThree()

downSites = []
count = 0

if len(data) > 0:
    for item in data:
        # print(item)
        # Only send an email if check has failed more than 3 times and only every 3 checks to minimize emails
        if item['downCount'] >= 3 and item['downCount'] % 3 == 0:
            count += 1
            downSites.append(item)
    if len(downSites) > 0:
        oe.outage(downSites, count)
