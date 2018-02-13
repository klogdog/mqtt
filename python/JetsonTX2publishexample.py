#example for Jetson TX2

import paho.mqtt.client as mqtt


#edit these to match your settings
mqttServer = "localhost" #use localhost as default
mqttPort = "1883" #use 1883 as default
mqttKeepAlive = 60 #use 60 as default
mqttUsername = "user"
mqttPassword = "password"
mqttTopic = "topic"
mqttClientID = "mqttClientID"
mqttPayload = "somepayload"
authorizationDictionary =  {‘username’:”<mqttUsername>”, ‘password’:”<mqttPassword>”}

#use this function to send a single message
single(mqttTopic, payload= mqttPayload, qos=0, retain=False, hostname=mqttServer,
    port=1883, client_id=mqttClientID, keepalive=60, will=None, auth=authorizationDictionary, tls=None,
    protocol=mqtt.MQTTv311)
