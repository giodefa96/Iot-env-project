from flask import Flask
from flask_mqtt import Mqtt
from utilities import utility
import topicname


import json
from dotenv import load_dotenv
import os


load_dotenv()


app = Flask(__name__)

with open('config/config.json') as config_file:
    config_data = json.load(config_file)
    
mqtt_settings = config_data['mqtt_settings']
app.config.update(mqtt_settings)

mqtt = Mqtt(app)



@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected with result code " + str(rc), end="\n\n\n")
        subscribe(topicname.first_call)
        subscribe(topicname.second_call)
        subscribe(topicname.test)
    else:
        print("Bad connection. Returned code=", rc)
        
        
@mqtt.on_disconnect()
def handle_disconnect(client, userdata, rc):
    print("Disconnecting reason: " + str(rc))
    
    
@mqtt.on_message()
def handle_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    print("Message from " + data.get("topic") + ":\n " + data.get("payload"), flush=True)
    utility.handle_topic(data)

def subscribe(topic, qos=0):
    mqtt.subscribe(topic, qos)    


def publish(topic, message):
    mqtt.publish(topic, message)
    print("\nPublished message: ", flush=True)
    print(message, end="\n\n", flush=True)
    print("topic: ")
    print(topic, end="\n\n", flush=True)
    
    
@mqtt.on_subscribe()
def handle_subscribe(client, userdata, mid, qos):
    print("Subscribe mid value: " + str(mid))

if __name__ == "__main__":
    
    app.run(host="0.0.0.0", port=os.getenv("PORT"), debug=False, use_reloader=False)