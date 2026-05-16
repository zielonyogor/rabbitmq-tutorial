import sys
import pika

EXCHANGE = 'events_ex'

BINDING_KEYS = {
    'order':  'order.#',
    'alerts': '*.failed.*',
    'eu':     '#.eu',
    'all':    '#',
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in BINDING_KEYS:
        print("Usage: python subscriber.py <mode>")
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

    channel.exchange_declare(exchange=EXCHANGE, exchange_type='topic', durable=True)

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange=EXCHANGE, queue=queue_name, routing_key=binding_key)

    def on_event(ch, method, properties, body):
        print(f"[{mode}] {method.routing_key} → {body.decode()}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue=queue_name, on_message_callback=on_event, auto_ack=False)

    print(f"[*] Subscriber '{mode}' ready (binding: {binding_key}). CTRL+C to stop.")
    channel.start_consuming()


if __name__ == "__main__":
    main()
