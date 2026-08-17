nats context add smarthouse_nats -s nats://smarthouse_nats:4222 --select

nats stream add COMMANDS --subjects "COMMANDS.>" --ack --max-msgs=-1 --max-bytes=-1 --max-age=300s \
--storage file --retention limits --max-msg-size=-1 --discard=old --replicas=1 \
--max-msgs-per-subject=-1 --dupe-window=5m0s --no-allow-rollup --deny-delete --deny-purge

nats stream add EVENTS --subjects "EVENTS.>" --ack --max-msgs=-1 --max-bytes=-1 --max-age=300s \
--storage file --retention limits --max-msg-size=-1 --discard=old --replicas=1 \
--max-msgs-per-subject=-1 --dupe-window=5m0s --no-allow-rollup --deny-delete --deny-purge

nats kv add DEVICES --history=1
