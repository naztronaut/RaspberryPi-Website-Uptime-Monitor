import reporting_db as rdb


data = rdb.getDownTimeCountsGreaterThanThree()

for item in data:
    print(item)