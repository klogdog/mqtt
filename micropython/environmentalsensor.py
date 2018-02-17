from sht30 import SHT30
import time
from wifi import wifi_connect
from umqtt.simple import MQTTClient
mqttServer = "mqttServer"
mqttPort = "1883"
mqttKeepAlive = 60
mqttUsername = "mqttUsername"
mqttPassword = "mqttPassword"
mqttTopic = "mqttTopic"
mqttClientID = "123456"
wifissid = "wifissid"
wifiPassword = "wifiPassword"
sensor = SHT30()
wifi_connect(wifissid,wifiPassword)
try:
  client = MQTTClient("856494",mqttServer, port=1883, user= mqttUsername, password= mqttPassword)
  client.connect()
except:
  print("connection error")
  time.sleep(5)
  machine.reset()  

while True:
  temperature, humidity = sensor.measure()
  mqttMessage = str(temperature) + '/' + str(humidity)
  try:
    client.publish(mqttTopic, mqttMessage)
  except:
    print("unhandled exception")
    time.sleep(5)
    machine.reset()
  time.sleep(10)
