"""
Task 1 — producer starter code.
Fill in every section marked TODO.
"""
import sys
import pika


def main():
    message = sys.argv[1] if len(sys.argv) > 1 else "Hello!"

    # TODO: Create a BlockingConnection.
    # Use pika.ConnectionParameters with host, port, and
    # pika.PlainCredentials('student', 'student123').
    connection = None
    channel = None

    # TODO: Declare a durable queue named 'hello_queue'.

    # TODO: Publish `message` (encode to bytes) to the default exchange.
    # Hint: exchange='', routing_key='hello_queue', delivery_mode=2.

    print(f"[x] Sent: {message}")

    # TODO: Close the connection.


if __name__ == "__main__":
    main()
