"""
Task 2 — worker consuming from 'task_queue'.
Fill in every section marked TODO.
"""
import pika

EXCHANGE = 'logs_ex'


def on_message(channel, method, properties, body):
    print(f"[task_worker] Received: {body.decode()}")
    # TODO: ACK the message.


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='localhost', port=5672,
            credentials=pika.PlainCredentials('student', 'student123')
        )
    )
    channel = connection.channel()

    # TODO: Declare the direct exchange EXCHANGE and durable queue 'task_queue'.
    # TODO: Bind 'task_queue' to EXCHANGE with routing_key='info'.

    # TODO: Set prefetch_count=1.

    # TODO: Register on_message for 'task_queue' with auto_ack=False.

    print("[*] Worker ready. CTRL+C to stop.")

    # TODO: Start consuming.


if __name__ == "__main__":
    main()
