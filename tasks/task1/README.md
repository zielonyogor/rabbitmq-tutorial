# Task 1 — Hello Queue (5 points)

**Estimated time:** 5 minutes

```
[producer.py] ──► (hello_queue) ──► [consumer.py]
```

Fill in the `TODO` sections in both files.

**Connection:** `localhost:5672`, user `student`, password `student123`

## producer.py
- Connect, declare a **durable** queue `hello_queue`
- Publish `sys.argv[1]` to the default exchange (`""`) with `delivery_mode=2`
- Print `[x] Sent: <message>` and close the connection

## consumer.py
- Connect, declare the same queue, set `prefetch_count=1`
- Callback: print `[x] Received: <message>` and send a manual ACK
- Start consuming

## Run

From the project root:

```bash
docker compose run --rm app python tasks/task1/consumer.py            # Terminal 1
docker compose run --rm app python tasks/task1/producer.py "Hello!"   # Terminal 2
```

Or, with local Python, `cd tasks/task1` first and run `python consumer.py` / `python producer.py "Hello!"`.
