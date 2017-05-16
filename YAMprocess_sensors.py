#!/usr/bin/python3
import paho.mqtt.client as mqtt
import re
import datetime
import json
import logging

#
# sensor_list.json File Format
# {
#        "28FFAE96641502A5":"Fish Tank",
#        "28FFE4D164150297":"Reptile Rack",
#        "28FFF58B641502E5":"Turtle Tank"
#}
sensor_list = json.loads(open('sensor_list.json').read())

#build a numeric (not float) timestamp with ms precision
def ts_ms(d):
    return int(d.timestamp()*1000)

# The callback when client receives a CANNACK from server
def on_connect(client, userdata, flags, rc):
    logging.info("Connected : " + str(rc))

    #subscribe on connect so we resubscibe if it is lost and reconnects
    client.subscribe("YarraRiverReptiles/#")

last = {"temperature":{}, "flow":{}}

#The callback when PUBLISH received from server
def on_message(client, userdata, msg):
    time_now = datetime.datetime.now()
    if (re.search(r'data/temperature', msg.topic)):
        ma = re.search(r'(.*)=(.*)C', msg.payload.decode("utf-8"))

        if ma:
            if ma.group(1) in sensor_list:
                sensor = ma.group(1)
                temperature = ma.group(2)
                name = sensor_list[sensor]
                if name not in last["temperature"] or last["temperature"][name] < time_now - datetime.timedelta(minutes=4, seconds=50):
                    data = {"name" : name,
                            "time_ms" : ts_ms(time_now),
                            "time_str" : time_now.strftime('%Y-%m-%d %H%M%S'),
                            "temperature" : temperature,
                            "ID" : sensor}
                    logging.info(json.dumps(data))
                    client.publish("YarraRiverReptiles/tanks/"+name+"/temperature", json.dumps(data))
                    last["temperature"][name] = time_now
            else:
                logging.debug("Not found")
    elif re.search(r'data/flow', msg.topic):
        ma = re.search(r'Pin(.*) =(.*)L', msg.payload.decode("utf-8"))
        if ma:
                
            rate = temperature = ma.group(2)
            name = "Turtle Tank"
            
            if name not in last["flow"] or last["flow"][name] < time_now - datetime.timedelta(minutes=4, seconds=50):

                data = {"name" : name,
                        "time_ms" : ts_ms(time_now),
                        "time_str" : time_now.strftime('%Y-%m-%d %H%M%S'),
                        "flow" : rate,
                        "ID"   : ma.group(1)}
                logging.info(json.dumps(data))
                client.publish("YarraRiverReptiles/tanks/"+name+"/flow", json.dumps(data))
                last["flow"][name] = time_now
                
        else:
                logging.debug("Flow fail")
#    print(msg.topic+" "+str(msg.payload))

logging.basicConfig(format="%(asctime)s %(message)s", filename="YAM.log", level=logging.DEBUG)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("raspberrypi", 1883, 60)

client.loop_forever()
