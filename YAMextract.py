import boto3
import json
from boto3.dynamodb.conditions import Key, Attr

import datetime

#extract the data from a dynamoDB

class YAMextract():

    def __init__(self, table_name="YAM"):
        self.table_name = table_name
        self.aws = {}
        self.load_keys()
        self.connect()

    # load security AWS keys required to connect to dynamoDB.
    # Note, you need to set up permissions and store the keys in a clear text file.
    # If security is an issue this needs to be improved.
    def load_keys(self):
        ##### aws_keys.json
        {
            "Region":"ap-southeast-2",
            "AccessKey":"_your key_",
            "SecretKey":"_your key_"
        }

        self.aws_keys = json.loads(open("aws_keys.json").read())

    # connect using AWS keys.
    def connect(self):
    
        self.session = boto3.Session(region_name = self.aws_keys["Region"], aws_access_key_id=self.aws_keys["AccessKey"], aws_secret_access_key=self.aws_keys["SecretKey"])
        self.conn = self.session.resource('dynamodb')

    # retrieve data for last N days for all tanks.
    def getData(self, days=7):
        table = self.conn.Table(self.table_name)

        start = datetime.datetime.now()

        series = {}
        for d in range(days):
            date = start - datetime.timedelta(days=d)
            #build the key for each day in the last selected number of days
            #daykey is a GSI so we can query rather than scan making it much faster
            daykey = "%d%03d" % (date.timetuple()[0], date.timetuple()[7])
            data = table.query(IndexName='daykey-index',
                               KeyConditionExpression=Key('daykey').eq(int(daykey)))
            print(daykey, data["Count"])   
            # not assuming the db entries are in time order.
            for entry in data["Items"]:
                if entry["name"] not in series.keys():
                    series[entry["name"]] = {}
                if "temperature" in entry.keys():
                    series[entry["name"]][float(entry["time_ms"])/1000] = entry["temperature"]
        
        end = datetime.datetime.now()
        print("Elapsed ", end - start)

        return series

