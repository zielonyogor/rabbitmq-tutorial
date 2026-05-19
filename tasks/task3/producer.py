"""
Task 3 — topic exchange producer.
Fill in every section marked TODO.

Usage: python producer.py <routing_key> <message>
  python producer.py order.created.eu  "Order #1 placed"
  python producer.py payment.failed.us "Card declined"
"""
import sys
import pika

EXCHANGE = 'events_ex'


def main():
    if len(sys.argv) < 3:
        print("Usage: python producer.py <routing_key> <message>")
        sys.exit(1)

    routing_key = sys.argv[1]
    message = sys.argv[2]

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='localhost', port=5672,
            credentials=pika.PlainCredentials('student', 'student123')
        )
    )
    channel = connection.channel()

    # TODO: Declare a durable topic exchange named EXCHANGE.

    # TODO: Publish `message` (bytes) to EXCHANGE with the given routing_key.
    # Use delivery_mode=2.

    print(f"[x] Published [{routing_key}] {message}")
    connection.close()


if __name__ == "__main__":
    main()
