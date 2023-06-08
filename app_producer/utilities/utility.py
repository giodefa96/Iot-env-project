import topicname
import json
import pika
import datetime
from dotenv import load_dotenv
import time
import wsgi

load_dotenv()

from module.mysqldb import Database

def handle_topic(data):
    topic = data.get("topic")
    payload = json.loads(data.get("payload"))
    payload['date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print("Topic: " + topic, flush=True)
    print("payload: ", payload,type(payload), flush=True)
    if topic == topicname.first_call:
        print("First call from master", flush=True)
        check_already_present = retrive_info_from_db(payload.get("ip"), payload.get("date"))
        print(check_already_present, flush=True)
        if not check_already_present:
            # aggiungere task nella coda
            send_message_to_queue(json.dumps(payload), queue_name='save_to_db')
        else:
            print("Device already present in db", flush=True)
            
    if topic == topicname.second_call:
        # controlliamo nel db se è tutto ok, quindi dobbiamo fare una query al db e vedere se ci sono errori o altro
        print("retrieve info from db", flush=True)
        info = retrive_info_from_db(payload.get("ip"))
        print(info, flush=True)
        time.sleep(5)
        
        if info:
            print("Info retrieved from db", flush=True)
            # se è tutto ok, allora possiamo inviare il messaggio
            wsgi.publish(topicname.response_second_call, "1")
            
        else:
            wsgi.publish(topicname.response_second_call, "0")
            
    if topic == topicname.test:
        print("Test message", flush=True)


def retrive_info_from_db(id, data=None):
    
    with open('config/config.json') as config_file:
        config_data = json.load(config_file)
    
    user_dict = config_data['mysql_settings']
    print("user_dict", flush=True)
    if data:
        print("Retrive info from db with data", flush=True)
        with Database(**user_dict) as db:
            db.execute("SELECT * FROM iot_devices WHERE ip = %s AND date = %s ", (id,data))
            return db.fetchall()
    else:
        with Database(**user_dict) as db:
            db.execute("SELECT * FROM iot_devices WHERE ip = %s", (id,))
            return db.fetchall()
    
    
def send_message_to_queue(message, queue_name='hello'):
    credentials = pika.PlainCredentials(username='user', password='password')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbimqServer',credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_publish(exchange='...',
                      routing_key=queue_name,
                      body=message,properties=pika.BasicProperties(
                         delivery_mode = pika.spec.PERSISTENT_DELIVERY_MODE
                      ))
    print(" [x] Sent '" + message + "'", flush=True)
    connection.close()

