from boto import dynamodb2
from boto.dynamodb2.table import Table
import boto
import json

table_name = "YAM_YRR"


##### aws_keys.json 
{
	"Region":"ap-southeast-2",
	"AccessKey":"_your key_",
        "SecretKey":"_your key_"
}

aws = json.loads(open("aws_keys.json").read())

conn = dynamodb2.connect_to_region(aws["Region"], aws_access_key_id=aws["AccessKey"], aws_secret_access_key=aws["SecretKey"])

table = Table(table_name, connection=conn)

data = table.query_2(name__eq="Temp.Hatchy")

