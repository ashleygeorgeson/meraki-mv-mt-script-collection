import pika
 
credentials = pika.PlainCredentials("guest", "guest")
conn_params = pika.ConnectionParameters("localhost",
                                        port=5672,
                                        credentials=credentials)
conn_broker = pika.BlockingConnection(conn_params)
channel = conn_broker.channel()
channel.exchange_declare(exchange="amq.topic",
                         exchange_type="topic",
                         durable=True)
channel.queue_declare(queue="mv-queue",
                      durable=True,
                      auto_delete=True)
channel.queue_bind(queue="mv-queue",
                   exchange="amq.topic",
                   routing_key=".merakimv.*.*")
 
def msg_consumer(channel, method, header, body):
    channel.basic_ack(delivery_tag=method.delivery_tag)
    if body == b"quit":
        channel.basic_cancel(consumer_tag="mv-consumer")
        channel.stop_consuming()
    else:
        print(method.routing_key.split('.')[2], body)
    return

'''
channel.basic_consume(msg_consumer,
                      queue="mv-queue",
                      consumer_tag="mv-consumer")
'''

channel.basic_consume("mv-queue",
                      msg_consumer,
                      consumer_tag="mv-consumer")

channel.start_consuming()