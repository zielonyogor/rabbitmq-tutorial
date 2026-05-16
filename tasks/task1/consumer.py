"""
Task 1 — consumer starter code.
Fill in every section marked TODO.
"""
import pika


def on_message(channel, method, properties, body):
    # TODO: Print the received message.
    # TODO: Send a manual ACK.
    pass


def main():
    # TODO: Create a BlockingConnection (same credentials as producer).
    connection = None
    channel = None

    # TODO: Declare the same durable queue 'hello_queue'.

    # TODO: Set prefetch_count=1 with basic_qos.

    # TODO: Register on_message as the callback for 'hello_queue'.
    # Use auto_ack=False so you handle ACKs manually.

    print("[*] Waiting for messages. Press CTRL+C to stop.")

    # TODO: Start consuming.


if __name__ == "__main__":
    main()
