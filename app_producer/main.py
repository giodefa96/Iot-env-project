# from connect_to_db import ClientInfluxDB
# from mqtt_subscriber import Mqtt_Subscriber
import paho.mqtt.publish as publish
import random
import psutil

# from threading import Thread
# import os

# from dotenv import load_dotenv

# load_dotenv()

import time

# url = os.getenv("INFLUXDB_URL")
# token = os.getenv("INFLUXDB_TOKEN")
# org = os.getenv("INFLUXDB_ORG")
# bucket = os.getenv("INFLUXDB_BUCKET")

# client_infx = ClientInfluxDB(url, token, org, bucket)


# def temp_thread_function():
    
#     mqtt_sub = Mqtt_Subscriber("test.mosquitto.org","temperature_camera_nostra")
    
#     while True:
        
#         tmp_value = mqtt_sub.topic_sub()
#         client_infx.write_single_value(tmp_value, "temp_camera", "temperature")
#         print("temp camera: ", tmp_value, "°C")


# def humidity_thread_function():
    
#     mqtt_sub = Mqtt_Subscriber("test.mosquitto.org","umidità")
    
#     while True:
#         humidity_value = mqtt_sub.topic_sub()
#         client_infx.write_single_value(humidity_value, "humidity_camera", "humidity") 
#         print("humidity camera: ", humidity_value, "%")


# def rssi_thread_function():
    
#     mqtt_sub = Mqtt_Subscriber("test.mosquitto.org","rssi")
    
#     while True:
#         rssi_value = mqtt_sub.topic_sub()
#         client_infx.write_single_value(rssi_value, "rssi_camera", "rssi") 
#         print("rssi camera: ", rssi_value, "dBm")


# def moisture_thread_function():
    
#     mqtt_sub = Mqtt_Subscriber("test.mosquitto.org","moisture")
    
#     while True:
#         moisture_value = mqtt_sub.topic_sub()
#         client_infx.write_single_value(moisture_value, "moisture_camera", "moisture") 
#         print("moisture camera: ", moisture_value, "%")



# temp_thread = Thread(target=temp_thread_function)
# huidity_thread = Thread(target=humidity_thread_function)
# rssi_thread = Thread(target=rssi_thread_function)
# moisture_thread = Thread(target=moisture_thread_function)



# temp_thread.start()
# huidity_thread.start()
# rssi_thread.start()
# moisture_thread.start()

if __name__ == "__main__":
    topic = 'computer/macbookpro'
    while True:
        publish.single(topic, payload=f"mac_cpu_temp perc={psutil.cpu_percent()}", qos=0, retain=False,auth = {'username':'', 'password':''}, hostname="",
               port=1883, client_id="", keepalive=60)
        print("message sent", flush=True)
        time.sleep(1)