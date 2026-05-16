"""
Task 2 — dedicated error handler (consumes from 'error_queue').
Fill in every section marked TODO.
"""
import pika

EXCHANGE = 'logs_ex'


def on_error(channel, method, properties, body):
    # TODO: Print the alert message.
    # TODO: ACK the message.
    pass


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='localhost', port=5672,
            credentials=pika.PlainCredentials('student', 'student123')
        )
    )
    channel = connection.channel()

    # TODO: Declare the same exchange and 'error_queue', bind them (routing_key='error').

    # TODO: Set prefetch_count=1.

    # TODO: Register on_error for 'error_queue' with auto_ack=False.

    print("[*] Error handler ready. CTRL+C to stop.")

    # TODO: Start consuming.


if __name__ == "__main__":
    main()
