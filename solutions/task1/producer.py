import sys
import pika


def main():
    message = sys.argv[1] if len(sys.argv) > 1 else "Hello!"

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='localhost', port=5672,
            credentials=pika.PlainCredentials('student', 'student123')
        )
    )
    channel = connection.channel()

    channel.queue_declare(queue='hello_queue', durable=True)

    channel.basic_publish(
        exchange='',
        routing_key='hello_queue',
        body=message.encode(),
        properties=pika.BasicProperties(delivery_mode=2),
    )

    print(f"[x] Sent: {message}")
    connection.close()


if __name__ == "__main__":
    main()
