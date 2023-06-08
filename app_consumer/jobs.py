from module.rabbitmq import PikaMassenger
from module.utility import handle_topic_from_quque

def start_consumer():
    def callback(ch, method, properties, body):
        print(" [x] %r:%r consumed" % (method.routing_key, body), flush=True)
        print("Devo smistare quello che mi arriva chiamando altre funzioni!", flush=True)
        ch.basic_ack(delivery_tag = method.delivery_tag)
        handle_topic_from_quque(method, body)

    with PikaMassenger() as consumer:
        consumer.consume(keys=['save_to_db','hello'], callback=callback)