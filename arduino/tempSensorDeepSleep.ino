#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <WEMOS_SHT3X.h>

SHT3X sht30(0x45);
#define SLEEP_DELAY_IN_SECONDS  30
const int sleepTime = 600; 
unsigned long previousMillis = 0; 
const long interval = 2000; 
const char* ssid = "SSID";
const char* password = "WIFIPASSWORD";
float humidity, temp_f;
const char* mqtt_server = "mqtt_server";
const char* mqtt_username = "mqtt_username";
const char* mqtt_password = "mqtt_password";
const char* mqtt_topic = "sensors/environmental/bedroom/temperature,humidity";

WiFiClient espClient;
PubSubClient client(espClient);


String dataString;
char charBuf[100];


void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();
}


void reconnect() {
  //WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    setup_wifi();
  }
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP8266_Client", mqtt_username, mqtt_password)) {
      Serial.println("connected");
    } else {
      Serial.print("MQTT connection failed, retry count: ");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void getTemperature() {
    sht30.get();   
    humidity = sht30.humidity;    
    temp_f = sht30.fTemp;
  
}


void loop() {

}

void setup() {
  // setup serial port
  Serial.begin(115200);
  pinMode(D0, WAKEUP_PULLUP);
  // setup WiFi
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
    if (!client.connected()) {
    reconnect();
  }
  client.loop();
  getTemperature();
  dataString =  temp_f + String("/")+ humidity;
  dataString.toCharArray(charBuf, 150);
  Serial.println(charBuf);
  client.publish(mqtt_topic, charBuf );
  delay(10000);
  ESP.deepSleep(sleepTime * 1000000);
}

