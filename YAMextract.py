from boto import dynamodb2
from boto.dynamodb2.table import Table
import boto
import json

import datetime

class YAMextract():

    def __init__(self, table_name="YAM_YRR"):
        self.table_name = table_name
        self.aws = {}
        self.load_keys()
        self.connect()


    def load_keys(self):
        ##### aws_keys.json
        {
            "Region":"ap-southeast-2",
            "AccessKey":"_your key_",
            "SecretKey":"_your key_"
        }

        self.aws_keys = json.loads(open("aws_keys.json").read())

    def connect(self):
    
        self.conn = dynamodb2.connect_to_region(self.aws_keys["Region"], aws_access_key_id=self.aws_keys["AccessKey"], aws_secret_access_key=self.aws_keys["SecretKey"])

    def getData(self, days=90):
        table = Table(self.table_name, connection=self.conn)

        start_time = datetime.datetime.now() - datetime.timedelta(days=days)
        time_ms = int(start_time.timestamp() * 1000) # TODO cleanup


#data = table.query_2(name__eq="Temp.Hatchy")
        data = table.scan(time_ms__gte=time_ms)

        series = {}
        # not assuming the db entries are in time order.
        for entry in data:
            print(entry["name"])
            if entry["name"] not in series.keys():
                series[entry["name"]] = {}
            series[entry["name"]][float(entry["time_ms"])/1000] = entry["temperature"]

        return series

