import pika

EXCHANGE = 'logs_ex'


def on_error(channel, method, properties, body):
    print(f"[ERROR HANDLER] ALERT: {body.decode()}")
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
    channel.queue_declare(queue='error_queue', durable=True)
    channel.queue_bind(exchange=EXCHANGE, queue='error_queue', routing_key='error')

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='error_queue', on_message_callback=on_error, auto_ack=False)

    print("[*] Error handler ready. CTRL+C to stop.")
    channel.start_consuming()


if __name__ == "__main__":
    main()
