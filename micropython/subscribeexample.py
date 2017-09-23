from wifi import wifi_connect
from umqtt.simple import MQTTClient
import machine
import time



mqttServer = "mqttServer"
mqttPort = "1883"
mqttKeepAlive = 60
mqttUsername = "mqttUsername"
mqttPassword = "mqttPassword"
mqttTopic = "mqttTopic"
mqttClientID = "123456"
wifissid = "wifissid"
wifiPassword = "wifiPassword"

wifi_connect(wifissid,wifiPassword)




def subscribeCallback(topic, msg):
    print((topic, msg))

client = MQTTClient(mqttClientID,mqttServer, port=1883, user= mqttUsername, password= mqttPassword)
client.set_callback(subscribeCallback)
client.connect()
client.subscribe(mqttTopic)
while True:
            client.check_msg()
            time.sleep(10)
