"""
Task 3 — topic exchange subscriber.
Fill in every section marked TODO.

Usage: python subscriber.py <mode>
  python subscriber.py order    # binding: order.#
  python subscriber.py alerts   # binding: *.failed.*
  python subscriber.py eu       # binding: #.eu
"""
import sys
import pika

EXCHANGE = 'events_ex'

# TODO: Fill in the correct binding key for each mode.
BINDING_KEYS = {
    'order':  None,   # TODO
    'alerts': None,   # TODO
    'eu':     None,   # TODO
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in BINDING_KEYS:
        print(f"Usage: python subscriber.py <mode>")
        print(f"  modes: {', '.join(BINDING_KEYS)}")
        sys.exit(1)

    mode = sys.argv[1]
    binding_key = BINDING_KEYS[mode]

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='localhost', port=5672,
            credentials=pika.PlainCredentials('student', 'student123')
        )
    )
    channel = connection.channel()

    # TODO: Declare the durable topic exchange EXCHANGE.

    # TODO: Declare an exclusive, auto-delete queue with an empty name.
    # Store the generated queue name from result.method.queue.
    queue_name = None

    # TODO: Bind queue_name to EXCHANGE using binding_key.

    def on_event(ch, method, properties, body):
        # TODO: Print "[<mode>] <routing_key> → <message>" and ACK.
        pass

    # TODO: Register on_event for queue_name with auto_ack=False.

    print(f"[*] Subscriber '{mode}' ready (binding: {binding_key}). CTRL+C to stop.")

    # TODO: Start consuming.


if __name__ == "__main__":
    main()
