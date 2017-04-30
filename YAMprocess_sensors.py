#!/usr/bin/python3
import paho.mqtt.client as mqtt
import re
import time
import json

#
# sensor_list.json File Format
# {
#        "28FFAE96641502A5":"Fish Tank",
#        "28FFE4D164150297":"Reptile Rack",
#        "28FFF58B641502E5":"Turtle Tank"
#}
sensor_list = json.loads(open('sensor_list.json').read())

# The callback when client receives a CANNACK from server
def on_connect(client, userdata, flags, rc):
    print("Connected : " + str(rc))

    #subscribe on connect so we resubscibe if it is lost and reconnects
    client.subscribe("YarraRiverReptiles/#")


#The callback when PUBLISH received from server
def on_message(client, userdata, msg):
    if (re.search(r'data/temperature', msg.topic)):
        ma = re.search(r'(.*)=(.*)C', msg.payload.decode("utf-8"))
        if ma:
            if ma.group(1) in sensor_list:
                sensor = ma.group(1)
                temperature = ma.group(2)
                name = sensor_list[sensor]
                
                data = {"name" : name,
                        "time" : time.strftime('{%Y-%m-%d %H%M%S}'),
                        "temperature" : temperature,
                        "ID" : sensor}
                print(json.dumps(data))
                client.publish("YarraRiverReptiles/tanks/"+name+"/temperature", json.dumps(data))
            else:
                print("Not found")
    elif re.search(r'data/flow', msg.topic):
        ma = re.search(r'Pin(.*) =(.*)L', msg.payload.decode("utf-8"))
        if ma:
            rate = temperature = ma.group(2)
            name = "Turtle Tank"
            data = {"name" : name,
                    "time" : time.strftime('{%Y-%m-%d %H%M%S}'),
                    "flow" : rate,
                    "ID"   : ma.group(1)}
            print(json.dumps(data))
            client.publish("YarraRiverReptiles/tanks/"+name+"/flow", json.dumps(data))
        else:
                print("Flow fail")
#    print(msg.topic+" "+str(msg.payload))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("raspberrypi", 1883, 60)

client.loop_forever()
