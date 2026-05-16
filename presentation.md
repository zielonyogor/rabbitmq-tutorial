# RabbitMQ — Practical Introduction
### Technologies of Software Development | Master SE

---

## Slide 1 — What Problem Does It Solve?

**Synchronous coupling is fragile:**

```
User → [Order Service] → [Inventory Service] → [Payment Service] → [Email Service]
```

- If any service is slow or down, the whole chain fails
- Services must be available at the same time
- Hard to scale individual parts

**Message broker decouples producers from consumers:**

```
Order Service → [Queue] → Inventory Service
                       → Payment Service
                       → Email Service
```

Each service works at its own pace. Failures are isolated.

---

## Slide 2 — RabbitMQ in One Picture

```
Producer ──► Exchange ──► Queue ──► Consumer
                │
                └──► Queue ──► Consumer
```

| Component    | Role                                                        |
|--------------|-------------------------------------------------------------|
| **Producer** | Application that sends messages                             |
| **Exchange** | Receives messages and routes them to queues (like a router) |
| **Queue**    | Buffer that stores messages until consumed                  |
| **Consumer** | Application that receives and processes messages            |
| **Binding**  | Rule that links an exchange to a queue                      |
| **Routing Key** | Label on a message used by exchanges to route it         |

---

## Slide 3 — The Four Exchange Types

### Direct Exchange
Routes messages to queues where the **binding key == routing key** exactly.

```
Exchange(direct) ──[routing_key=error]──► queue_errors
                 ──[routing_key=info]───► queue_logs
```

Use case: task distribution, error routing.

---

### Fanout Exchange
**Broadcasts** to ALL bound queues. Ignores routing keys.

```
Exchange(fanout) ──► queue_A
                 ──► queue_B
                 ──► queue_C
```

Use case: notifications, cache invalidation, live event feeds.

---

### Topic Exchange
Routes based on **pattern matching** on the routing key (dot-separated words).

- `*` matches exactly one word
- `#` matches zero or more words

```
routing_key = "order.created.eu"

exchange ──[order.#]──────► order_service   ✓ matches
         ──[*.created.*]───► analytics      ✓ matches
         ──[payment.#]─────► payment_svc    ✗ no match
```

Use case: event-driven microservices, fine-grained subscriptions.

---

### Headers Exchange
Routes based on **message header attributes** instead of routing key.
Rarely used in practice — topic exchange covers most cases.

---

## Slide 4 — Message Lifecycle

```
1. Producer connects and publishes a message to an exchange
2. Exchange applies routing rules → selects matching queues
3. Message is stored in the queue (persisted if durable)
4. Consumer connects and subscribes to the queue
5. Broker delivers the message
6. Consumer sends ACK (acknowledgment)
7. Broker removes the message from the queue
```

**What if the consumer crashes before ACK?**  
The broker re-queues the message and delivers it to another consumer.

**What if no queue matches?**  
Message is dropped (or sent to a dead-letter exchange if configured).

---

## Slide 5 — Durability & Acknowledgments

**Three layers of durability:**

| Setting                  | Meaning                                              |
|--------------------------|------------------------------------------------------|
| `durable=True` on queue  | Queue survives broker restart                        |
| `delivery_mode=2`        | Message is persisted to disk                         |
| Manual ACK               | Message stays in queue until consumer confirms it    |

**Auto-ACK vs Manual ACK:**

```python
# Auto-ACK — message deleted immediately on delivery (fast, risky)
channel.basic_consume(queue='tasks', on_message_callback=cb, auto_ack=True)

# Manual ACK — message stays until you call basic_ack (safe)
def callback(ch, method, properties, body):
    process(body)
    ch.basic_ack(delivery_tag=method.delivery_tag)
```

---

## Slide 6 — Connection & Channel

```
TCP Connection
└── Channel 1  (lightweight virtual connection)
└── Channel 2
└── Channel 3
```

- **Connection**: one TCP connection per application instance
- **Channel**: multiplexed logical session inside a connection
- Create one channel per thread; don't share channels across threads

```python
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672,
        credentials=pika.PlainCredentials('student', 'student123'))
)
channel = connection.channel()
```

---

## Slide 7 — Quick Code Walkthrough

**Producer:**
```python
channel.queue_declare(queue='hello', durable=True)
channel.basic_publish(
    exchange='',           # default (direct) exchange
    routing_key='hello',   # queue name = routing key for default exchange
    body='Hello World!',
    properties=pika.BasicProperties(delivery_mode=2)
)
```

**Consumer:**
```python
channel.queue_declare(queue='hello', durable=True)

def on_message(ch, method, properties, body):
    print(f"Received: {body.decode()}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)   # don't send more than 1 msg at a time
channel.basic_consume(queue='hello', on_message_callback=on_message)
channel.start_consuming()
```

`basic_qos(prefetch_count=1)` ensures fair dispatch — busy workers don't get new messages until they finish the current one.

---

## Slide 8 — Management UI

RabbitMQ ships with a web UI at **http://localhost:15672**

- Credentials: `student` / `student123`
- See all exchanges, queues, bindings
- Publish and get messages manually
- Monitor message rates and consumer counts
- **Use this during the tasks to verify your work**

---

## Slide 9 — When to Use RabbitMQ

**Good fit:**
- Async task processing (image resize, email sending, report generation)
- Decoupling microservices
- Event-driven pipelines
- Work queues with multiple competing consumers

**Not a good fit:**
- You need exactly-once delivery with strict ordering at very high scale → Kafka
- Simple in-process job queue → Celery with Redis, BullMQ
- RPC where you need a synchronous response immediately

---

## Slide 10 — Summary

| Concept      | One-liner                                                  |
|--------------|------------------------------------------------------------|
| Queue        | Named buffer; stores messages in order                     |
| Exchange     | Router; decides which queue(s) get the message             |
| Binding      | Wires an exchange to a queue, optionally with a key        |
| Routing key  | Label on the message used by direct/topic exchanges        |
| ACK          | Consumer's receipt that lets the broker discard the message|
| Prefetch     | Limits how many unacked messages a consumer holds at once  |

**Now over to you — 3 tasks, 45 minutes.**

---
