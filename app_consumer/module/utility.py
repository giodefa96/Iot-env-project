import os
import json

from dotenv import load_dotenv
load_dotenv()

from module.mysqldb import Database

def handle_topic_from_quque(method, body):
    body = json.loads(body)
    print(method, flush=True)
    if method.routing_key == 'save_to_db':
        save_data_to_db(body)


def save_data_to_db(data):
    print("Saving data into db", flush=True)
    with open('config.json') as config_file:
        config_data = json.load(config_file)
    
    user_dict = config_data['mysql_settings']
    
    print(user_dict, flush=True)
    
    with Database(**user_dict) as db:
        
        db.execute("INSERT INTO iot_devices (ip, type, sensor_type, rssi, position, coordinate, date) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                   (data.get("ip"), data.get("type"), data.get("sensor_type"), data.get("rssi"), data.get("position"), data.get("coordinate"), data.get("date")))
        db.commit()
        
        print(db.cursor.rowcount, "was inserted.")
        print("Data saved", flush=True)
        