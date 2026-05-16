import sys
import pika

EXCHANGE = 'events_ex'


def main():
    if len(sys.argv) < 3:
        print("Usage: python producer.py <routing_key> <message>")
        sys.exit(1)

    routing_key, message = sys.argv[1], sys.argv[2]

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='localhost', port=5672,
            credentials=pika.PlainCredentials('student', 'student123')
        )
    )
    channel = connection.channel()

    channel.exchange_declare(exchange=EXCHANGE, exchange_type='topic', durable=True)

    channel.basic_publish(
        exchange=EXCHANGE,
        routing_key=routing_key,
        body=message.encode(),
        properties=pika.BasicProperties(delivery_mode=2),
    )

    print(f"[x] Published [{routing_key}] {message}")
    connection.close()


if __name__ == "__main__":
    main()
