# Task 2 — Direct Exchange (10 points)

**Estimated time:** 10 minutes

```
              ┌─[error] ──► error_queue ──► error_worker.py
producer.py ──► logs_ex
              └─[info]  ──► task_queue  ──► worker.py
```

Fill in the `TODO` sections in all three files.

## producer.py
- Declare a **direct** exchange `logs_ex` and two durable queues
- Bind `error_queue` → routing key `error`, `task_queue` → routing key `info`
- Publish `sys.argv[2]` to `logs_ex` with routing key `sys.argv[1]`

## worker.py
- Declare the same exchange and `task_queue`, bind with key `info`
- Set `prefetch_count=1`, consume with manual ACK

## error_worker.py
- Declare the same exchange and `error_queue`, bind with key `error`
- Consume with manual ACK, print `[ERROR HANDLER] ALERT: <message>`

## Run

From the project root:

```bash
docker compose run --rm app python tasks/task2/worker.py                            # Terminal 1
docker compose run --rm app python tasks/task2/error_worker.py                      # Terminal 2
docker compose run --rm app python tasks/task2/producer.py info  "User logged in"   # Terminal 3
docker compose run --rm app python tasks/task2/producer.py error "DB is down"
```

Or, with local Python, `cd tasks/task2` first and run the scripts as `python worker.py`, etc.
