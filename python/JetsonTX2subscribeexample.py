#example for Jetson TX2

import paho.mqtt.client as mqtt


#edit these to match your settings
mqttServer = "localhost" #use localhost as default
mqttPort = "1883" #use 1883 as default
mqttKeepAlive = 60 #use 60 as default
mqttUsername = "mqttUsername"
mqttPassword = "mqttPassword"
mqttTopic = "mqttTopic"
mqttClientID = "mqttClientID"



def on_connect(client, userdata, flags, rc):
    client.subscribe(mqttTopic)

#use this function to do stuff when you receive a message
#when a message is received it will execute the commands in this function
def on_message(client, userdata, msg):
    measurement = msg.payload
    topic = msg.topic
    print topic
    print measurement 


client = mqtt.Client()
client.username_pw_set(mqttUsername,mqttPassword)
client.on_connect = on_connect
client.on_message = on_message


client.connect(mqttServer, mqttPort, mqttKeepAlive)


client.loop_forever()
