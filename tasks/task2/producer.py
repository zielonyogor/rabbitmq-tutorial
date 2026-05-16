"""
Task 2 — producer starter code.
Fill in every section marked TODO.

Usage: python producer.py <severity> <message>
  python producer.py error "Disk full"
  python producer.py info  "User logged in"
"""
import sys
import pika

EXCHANGE = 'logs_ex'


def get_channel():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='localhost', port=5672,
            credentials=pika.PlainCredentials('student', 'student123')
        )
    )
    return connection, connection.channel()


def setup_topology(channel):
    # TODO: Declare a durable direct exchange named EXCHANGE.

    # TODO: Declare durable queues 'error_queue' and 'task_queue'.

    # TODO: Bind 'error_queue' to EXCHANGE with routing_key='error'.
    # TODO: Bind 'task_queue'  to EXCHANGE with routing_key='info'.
    pass


def main():
    if len(sys.argv) < 3:
        print("Usage: python producer.py <severity> <message>")
        sys.exit(1)

    severity = sys.argv[1]
    message = sys.argv[2]

    connection, channel = get_channel()
    setup_topology(channel)

    # TODO: Publish `message` (bytes) to EXCHANGE with routing_key=severity.
    # Use delivery_mode=2.

    print(f"[x] Sent [{severity}] {message}")
    connection.close()


if __name__ == "__main__":
    main()
