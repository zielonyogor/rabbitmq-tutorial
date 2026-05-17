# RabbitMQ Tutorial
### Technologies of Software Development — Master SE

---

## Structure

```
rabbitmq-tutorial/
├── presentation.md          ← lecture slides (15–30 min)
├── docker-compose.yml       ← RabbitMQ broker + app container
├── Dockerfile               ← Python image with pika installed
├── requirements.txt         ← Python dependencies (pika)
│
├── tasks/
│   ├── task1/               ★★★★★  5 pts  — Hello Queue
│   │   ├── README.md        ← task description & acceptance criteria
│   │   ├── producer.py      ← starter code (TODOs)
│   │   └── consumer.py
│   ├── task2/               ★★★★★★★★★★  10 pts  — Direct Exchange & Work Queue
│   │   ├── README.md
│   │   ├── producer.py
│   │   ├── worker.py
│   │   └── error_worker.py
│   └── task3/               ★★★★★★★★★★★★★★★  15 pts  — Topic Exchange
│       ├── README.md
│       ├── producer.py
│       └── subscriber.py
│
└── solutions/               ← reference solutions (do not share until after lab)
    ├── task1/
    ├── task2/
    └── task3/
```

---

## Quick Start

### 1. Start RabbitMQ

```bash
docker compose up -d rabbitmq
```

Wait until `docker compose ps` shows the broker as **healthy** (usually 10–20 s), then open the management UI:
**http://localhost:15672** — login: `student` / `student123`

### 2. Run scripts

Use the pre-built `app` container to run any script:

```bash
# producer
docker compose run --rm app python tasks/task1/producer.py "Hello"

# consumer (Ctrl+C to stop)
docker compose run --rm app python tasks/task1/consumer.py
```

> **Local Python:** if you have Python 3 installed you can also run scripts directly after `pip install -r requirements.txt`.

### 3. Work through tasks in order

Each task folder has a `README.md` with the full description, requirements,
and acceptance criteria. The starter files contain `# TODO` markers where you
need to fill in code.

---

## Scoring

| Task | Topic                          | Points |
|------|--------------------------------|--------|
| 1    | Hello Queue (default exchange) | 5      |
| 2    | Direct exchange + work queue   | 10     |
| 3    | Topic exchange + pub/sub       | 15     |
| **Total** |                           | **30** |

---

## RabbitMQ Cheat Sheet

```python
import pika

# Connect
conn = pika.BlockingConnection(
    pika.ConnectionParameters('localhost', 5672,
        credentials=pika.PlainCredentials('student', 'student123')))
ch = conn.channel()

# Declare queue (idempotent)
ch.queue_declare(queue='my_queue', durable=True)

# Declare exchange
ch.exchange_declare(exchange='my_ex', exchange_type='direct', durable=True)
# exchange_type: 'direct' | 'fanout' | 'topic' | 'headers'

# Bind queue to exchange
ch.queue_bind(exchange='my_ex', queue='my_queue', routing_key='my_key')

# Publish
ch.basic_publish(
    exchange='my_ex',          # '' = default exchange
    routing_key='my_key',
    body=b'hello',
    properties=pika.BasicProperties(delivery_mode=2))  # persistent

# Consume (manual ACK)
def callback(ch, method, properties, body):
    print(body.decode())
    ch.basic_ack(delivery_tag=method.delivery_tag)

ch.basic_qos(prefetch_count=1)
ch.basic_consume(queue='my_queue', on_message_callback=callback, auto_ack=False)
ch.start_consuming()

# Exclusive queue (auto-deleted on disconnect, for pub/sub)
result = ch.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
```

### Exchange type quick reference

| Type    | Routing logic                            | Typical use case         |
|---------|------------------------------------------|--------------------------|
| default | routing_key == queue name                | Simple point-to-point    |
| direct  | binding_key == routing_key (exact match) | Log levels, task routing |
| fanout  | broadcast to all bound queues            | Notifications, cache bust|
| topic   | pattern match with `*` and `#`           | Event-driven services    |

### Topic wildcard rules
- `*` matches **exactly one** word between dots
- `#` matches **zero or more** words

```
Routing key:     order.created.eu
Matches:         order.#          ✓
                 *.created.*      ✓
                 #.eu             ✓
                 order.*          ✗  (two words after order)
                 *.eu             ✗  (one word before eu, but key has two)
```
