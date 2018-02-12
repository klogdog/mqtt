#subscribes to an mqtt client and writes the incoming messages to influxDB dynamically

#for submitting data to influx db format is measurement, tags{tags}, fields{fields} 
#for topic format coming out of the microcontroller should be sensors/sensortype/location/measurementtype1,measurementtype2,measurementtypeN 
#for data format should be datafrom_measurementtype1/datafrom_measurementtype2/datafrom_measurementtypeN


import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient



mqttServer = "localhost" #use localhost as default
mqttPort = "1883" #use 1883 as default
mqttKeepAlive = 60 #use 60 as default
mqttUsername = "user"
mqttPassword = "password"
mqttTopic = "topic"
#mqttClientID = "mqttClientID"



influxDBserver = "localhost" #use localhost as default
influxDBport = "8086" #use 8086 as default
influxDBusername = "root" #use root as default
influxDBpassword = "root" #use root as default
influxDatabase = "sensorData"
#json_constructor takes the MQTT topic data, splits and reforms the data, and then constructs a valid json body formatted for influxdb 
def json_constructor(topic,measurement):
    # an empty dictionary to hold the fields
    dataHolder = {}
    #an empty list to hold the keys for the dictionary fields
    keys = []
    #an empty list to hold the values for the dictionary fields
    values = []
    #passing variables into the function
    topic = topic 
    measurement = measurement 
    #splitting topic into defined components
    sensortype = topic.split("/")[1]
    location = topic.split("/")[2]
    splitTopic = topic.split("/")[3]
    splitMeasurementType = splitTopic.split(",")
    splitMeasurement = measurement.split("/")
    dataHolder["measurement"] = sensortype
    dataHolder["tags"] = {'location': location}
    # this loop takes the split topics and arranges them into a key list and a value list
    # this allows an arbitrary set of of measurements to be submitted and transformed dynamically
    for i in range (0,len(splitMeasurementType)):
       measurementTypeHolder = splitMeasurementType[i]
       measurementHolder = splitMeasurement[i]
       keys.append(measurementTypeHolder)
       values.append(measurementHolder)
    # zip maps the two lists, keys and values, onto fields    
    fields = dict(zip(keys,values))
    dataHolder["fields"] = fields
    return dataHolder


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    #print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(mqttTopic)

# When a MQTT published message is received the payload of the MQTT message is written into the variable named measurement and the topic of the MQTT message is written into the variable named topic
# json_body calls json_constructor and passes it topic and measurement. json_body is then passed back the json data. The json data is then turned into 
# a valid json object and written to the influx database. 
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
