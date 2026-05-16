import sys
import pika

EXCHANGE = 'logs_ex'


def main():
    if len(sys.argv) < 3:
        print("Usage: python producer.py <severity> <message>")
        sys.exit(1)

    severity, message = sys.argv[1], sys.argv[2]

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='localhost', port=5672,
            credentials=pika.PlainCredentials('student', 'student123')
        )
    )
    channel = connection.channel()

    channel.exchange_declare(exchange=EXCHANGE, exchange_type='direct', durable=True)
    channel.queue_declare(queue='error_queue', durable=True)
    channel.queue_declare(queue='task_queue', durable=True)
    channel.queue_bind(exchange=EXCHANGE, queue='error_queue', routing_key='error')
    channel.queue_bind(exchange=EXCHANGE, queue='task_queue', routing_key='info')

    channel.basic_publish(
        exchange=EXCHANGE,
        routing_key=severity,
        body=message.encode(),
        properties=pika.BasicProperties(delivery_mode=2),
    )

    print(f"[x] Sent [{severity}] {message}")
    connection.close()


if __name__ == "__main__":
    main()
