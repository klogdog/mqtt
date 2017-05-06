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


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(mqttTopic)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    
    measurements = msg.payload
    topic = msg.topic
    temperature = float(measurements.split("/")[0])
    humidity = float(measurements.split("/")[1])
    location = topic.split("/")[1]
    sensortype = topic.split("/")[2]
    json_body = [
    {
        "measurement": sensortype,
        "tags": {
            "location": location,
        },
     
        "fields": {
            "temperature": temperature,
            "humidity" : humidity
        }
    }
    ]
    influx_client.write_points(json_body)
    print(msg.topic+" "+str(msg.payload))
    print json_body

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

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
