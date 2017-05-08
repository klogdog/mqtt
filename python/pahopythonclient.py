#for submitting data to influx db format is measurement, tags{tags}, fields{fields} 
#for topic format coming out of the microcontroller should be sensors/sensortype/location/measurementtype1,measurementtype2,measurementtypeN 
#for data format should be datafrom_measurementtype1/datafrom_measurementtype2/datafrom_measurementtypeN


import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient



mqttServer = "mqttServer"
mqttPort = "mqttPort" #use 1883 as default
mqttKeepAlive = "mqttKeepAliveTime" #use 60 as default
mqttUsername = "mqttUsername"
mqttPassword = "mqttPassword"
mqttTopic = "mqttTopic"
mqttClientID = "mqttClientID"


influxDBserver = "influxDBserver"
influxDBport = "influxDBport" #use 8086 as default
influxDBusername = "influxDBusername" #use root as default
influxDBpassword = "influxDBpassword" #use root as default
influxDatabase = "influxDatabase"

def json_constructor(topic,measurement):
    dataHolder = {}
    keys = []
    values = []
    topic = topic 
    measurement = measurement 
    sensortype = topic.split("/")[1]
    location = topic.split("/")[2]
    splitTopic = topic.split("/")[3]
    splitMeasurementType = splitTopic.split(",")
    splitMeasurement = measurement.split("/")
    dataHolder["measurement"] = sensortype
    dataHolder["tags"] = {'location': location}
    for i in range (0,len(splitMeasurementType)):
       measurementTypeHolder = splitMeasurementType[i]
       measurementHolder = splitMeasurement[i]
       keys.append(measurementTypeHolder)
       values.append(measurementHolder)
    fields = dict(zip(keys,values))
    dataHolder["fields"] = fields
    return dataHolder


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(mqttTopic)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    measurement = msg.payload
    topic = msg.topic
    json_body = json_constructor(topic,measurement)
    json_body = [json_body]
    influx_client.write_points(json_body)

influx_client = InfluxDBClient(influxDBserver, influxDBport, influxDBusername , influxDBpassword , influxDatabase)
client = mqtt.Client()
client.username_pw_set(mqttUsername,mqttPassword)
client.on_connect = on_connect
client.on_message = on_message


client.connect(mqttServer, mqttPort, mqttKeepAlive)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
