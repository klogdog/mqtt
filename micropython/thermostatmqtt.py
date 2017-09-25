#First generation working thermostat code 

from wifi import wifi_connect
from umqtt.simple import MQTTClient
import machine
import time
from machine import Pin



mqttServer = "mqttServer"
mqttPort = "1883"
mqttKeepAlive = 60
mqttUsername = "mqttUsername"
mqttPassword = "mqttPassword"
mqttTopic = "mqttTopic"
mqttClientID = "123456"
wifissid = "wifissid"
wifiPassword = "wifiPassword"
relayPin = Pin(5,Pin.OUT)
mqttTopic1 = "sensors/environmental/new/temperature,humidity"
mqttTopic2 = "heater"
mqttTopic3 = 'tempset'



wifi_connect(wifissid,wifiPassword)
heaterFlag = 0
temperature = b'90'
setTemperature = b'0'



def sub_cb(topic, msg):
    global heaterFlag
    global temperature
    global setTemperature
    if topic == b'heater':
        if msg == b'0':
            heaterFlag = 0
        if msg == b'1':
            heaterFlag = 1
    if topic == b'sensors/environmental/new/temperature,humidity':
       measurement = msg.split(b'/')
       temperature = measurement[0]
    if topic == b'tempset':
        setTemperature = msg






client = MQTTClient("123456",mqttServer, port=1883, user= mqttUsername, password= mqttPassword)
client.set_callback(sub_cb)
client.connect()
client.subscribe(mqttTopic1)
client.subscribe(mqttTopic2)
client.subscribe(mqttTopic3)
while True:
            client.check_msg()
            if heaterFlag == 1:
              if temperature < setTemperature:
               relayPin.value(1)
              else:
               relayPin.value(0)
            if heaterFlag == 0:
                relayPin.value(0)
            time.sleep(1)
