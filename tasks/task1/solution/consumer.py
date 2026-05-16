import pika


def on_message(channel, method, properties, body):
    print(f"[x] Received: {body.decode()}")
    channel.basic_ack(delivery_tag=method.delivery_tag)


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='localhost', port=5672,
            credentials=pika.PlainCredentials('student', 'student123')
        )
    )
    channel = connection.channel()

    channel.queue_declare(queue='hello_queue', durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='hello_queue', on_message_callback=on_message, auto_ack=False)

    print("[*] Waiting for messages. Press CTRL+C to stop.")
    channel.start_consuming()


if __name__ == "__main__":
    main()
