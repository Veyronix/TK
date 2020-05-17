import pika


def send():
    connection = pika.BlockingConnection(pika.ConnectionParameters('user:bitnami@localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='backend')
    channel.basic_publish(exchange='',
                          routing_key='backend',
                          body='Hello World!')
    print(" [x] Sent 'Hello World!'")
    pass


def receive():
    credentials = pika.PlainCredentials('user', 'bitnami')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='backend')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    channel.basic_consume(queue='backend', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
