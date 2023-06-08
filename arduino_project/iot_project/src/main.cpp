#include <Arduino.h>
#include "secret.h"
#include <WiFiNINA.h>
#include <ArduinoMqttClient.h>
#include <ArduinoJson.h>

WiFiClient wifiClient;
MqttClient mqttClient(wifiClient);

char ssid[] = SECRET_SSID;   // your network SSID (name)
char pass[] = SECRET_PASS;   // your network password

const char broker[] = MQTT_BROKERIP;
int port = MQTT_PORT;
const char mqtt_username[] = MQTT_USERNAME;
const char mqtt_password[] = MQTT_PASSWORD;

const char first_call[] = "mysql/hello_world";
const char second_call[] = "mysql/hello_master";
const char response_second_call[] = "mysql/response_hello_master";

// put function declarations here:
int myFunction(int, int);


void connectToWifi() {
  // attempt to connect to Wifi network:
  Serial.print("Attempting to connect to WPA SSID: ");
  Serial.println(ssid);
  while (WiFi.begin(ssid, pass) != WL_CONNECTED) {
    // failed, retry
    Serial.print(".");
    delay(5000);
  }

  Serial.println("You're connected to the network");
  Serial.println();
}


void connectToMqtt() {
  Serial.print("Attempting to connect to the MQTT broker: ");
  Serial.println(broker);
  mqttClient.setUsernamePassword(mqtt_username, mqtt_password);
  if (!mqttClient.connect(broker, port)) {
    Serial.print("MQTT connection failed! Error code = ");
    Serial.println(mqttClient.connectError());

    while (1);
  }

  Serial.println("You're connected to the MQTT broker!");
  Serial.println();
}


void sendingInitialMessage() {

  StaticJsonDocument<200> doc;
  IPAddress ip = WiFi.localIP();
  doc["ip"] = ip;
  doc["type"]   =  "master";
  doc["sensor_type"] = "test";
  doc["rssi"] = WiFi.RSSI();
  doc["position"] = "Cinisello Balsamo";
  doc["coordinate"] = "45.55";
  
  serializeJson(doc, Serial);

  Serial.print("Sending message to topic: ");
  Serial.println(first_call);
 
  mqttClient.beginMessage(first_call);
  mqttClient.print(doc.as<String>());
  mqttClient.endMessage();

}

void onMessageReceived(int messageSize)
{
  char inChar;
  while (mqttClient.available())
  {
    inChar = (char)mqttClient.read();  //get next character
    switch (inChar)
  {
    case '0': //if it is a 0
      Serial.println("Off");
      WiFi.disconnect();
      setup();
        break;
      case '1': //if it is a 1
        Serial.println("On");
        break;
      default:  //otherwise
        Serial.println("got something else");
        WiFi.disconnect();
        setup();
    }
    Serial.println();
    Serial.println();
  }
}

void onMqttMessage(int messageSize) {

  // we received a message, print out the topic and contents
  Serial.println("Received a message with topic :");
  Serial.print(mqttClient.messageTopic());
  Serial.print("', length ");
  Serial.print(messageSize);
  Serial.println(" bytes:");
  Serial.println();

}

void sendingControllMessage(){
  IPAddress ip = WiFi.localIP();
  StaticJsonDocument<200> doc;
  doc["ip"] = ip;
  serializeJson(doc, Serial);

  mqttClient.beginMessage(second_call);
  mqttClient.print(doc.as<String>());
  mqttClient.endMessage();

  // set the message receive callback
  mqttClient.onMessage(onMessageReceived);

  Serial.print("Subscribing to topic: ");
  Serial.println(response_second_call);
  Serial.println();

  // subscribe to a topic
  mqttClient.subscribe(response_second_call);

  // topics can be unsubscribed using:
  // mqttClient.unsubscribe(topic);
  Serial.print("Waiting for messages on topic: ");
  Serial.println(response_second_call);
  Serial.println();
 
}


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

  connectToWifi();

  connectToMqtt();

  sendingInitialMessage();

  delay(5000);

  sendingControllMessage();


  // chiamo la second call
  // e rimango in attesa che il server mi risponda così da poter continuare
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println("Starting loop");
  mqttClient.poll();
  delay(10000);
}


