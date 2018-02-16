#example for Jetson TX2

import time
import paho.mqtt.publish as mqtt


#edit these to match your settings
mqttServer = "mqttServer" #use localhost as default
mqttPort = "1883" #use 1883 as default
mqttKeepAlive = 60 #use 60 as default
mqttUsername = "mqttUsername"
mqttPassword = "mqttPassword"
mqttTopic = "mqttTopic"
mqttTopic2 = "mqttTopic2"
mqttClientID = "mqttClientID"
mqttPayload1 = 0
mqttPayload2 = 1
authorizationDictionary =  {'username':"<mqttUsername>", 'password':"<mqttPassword>"}

#use this function to send a single message
while True:
 time.sleep(5)
 mqtt.single(mqttTopic, payload= mqttPayload, qos=0, retain=False, hostname=mqttServer,
    port=1883, client_id=mqttClientID, keepalive=60, will=None, auth=authorizationDictionary, tls=None)
 mqtt.single(mqttTopic1, payload= mqttPayload2, qos=0, retain=False, hostname=mqttServer,
    port=1883, client_id=mqttClientID, keepalive=60, will=None, auth=authorizationDictionary, tls=None)
