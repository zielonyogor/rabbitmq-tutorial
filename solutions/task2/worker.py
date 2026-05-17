import pika

EXCHANGE = 'logs_ex'


def on_message(channel, method, properties, body):
    print(f"[task_worker] Received: {body.decode()}")
    channel.basic_ack(delivery_tag=method.delivery_tag)


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='localhost', port=5672,
            credentials=pika.PlainCredentials('student', 'student123')
        )
    )
    channel = connection.channel()

    channel.exchange_declare(exchange=EXCHANGE, exchange_type='direct', durable=True)
    channel.queue_declare(queue='task_queue', durable=True)
    channel.queue_bind(exchange=EXCHANGE, queue='task_queue', routing_key='info')

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='task_queue', on_message_callback=on_message, auto_ack=False)

    print("[*] Worker ready. CTRL+C to stop.")
    channel.start_consuming()


if __name__ == "__main__":
    main()
