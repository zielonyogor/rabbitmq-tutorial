# Task 3 — Topic Exchange (15 points)

**Estimated time:** 10 minutes

Routing key format: `<domain>.<event>.<region>`

```
              ┌─[order.#]    ──► subscriber.py order
producer.py ──► events_ex ─┼─[*.failed.*] ──► subscriber.py alerts
              └─[#.eu]      ──► subscriber.py eu
```

Fill in the `TODO` sections in both files.

## producer.py
- Declare a **topic** exchange `events_ex` (`durable=True`)
- Publish `sys.argv[2]` with routing key `sys.argv[1]`

## subscriber.py
Three modes via `sys.argv[1]`:

| Mode   | Binding key  |
|--------|--------------|
| order  | `order.#`    |
| alerts | `*.failed.*` |
| eu     | `#.eu`       |

- Declare an **exclusive** auto-delete queue: `result = channel.queue_declare(queue='', exclusive=True)`
- Bind it, then callback: print `[<mode>] <routing_key> → <message>` and ACK

**Tip:** `*` = one word, `#` = zero or more words

## Run

From the project root:

```bash
docker compose run --rm app python tasks/task3/subscriber.py order                           # Terminal 1
docker compose run --rm app python tasks/task3/subscriber.py alerts                          # Terminal 2
docker compose run --rm app python tasks/task3/producer.py order.created.eu  "Order #1"      # Terminal 3
docker compose run --rm app python tasks/task3/producer.py payment.failed.eu "Card error"
```

Or, with local Python, `cd tasks/task3` first and run the scripts as `python subscriber.py order`, etc.
