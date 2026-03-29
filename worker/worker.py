import redis
from app.config import STREAM_NAME, GROUP_NAME
from worker.processor import process_event
# import sys
# import os

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# Unique worker name (VERY IMPORTANT)
CONSUMER_NAME = "worker_1"

r = redis.Redis(host="localhost", port=6379, decode_responses=True)


def worker():
    print(f"{CONSUMER_NAME} started...")

    while True:
        messages = r.xreadgroup(
            groupname=GROUP_NAME,
            consumername=CONSUMER_NAME,
            streams={STREAM_NAME: ">"},
            count=1,
            block=5000
        )

        if messages:
            for stream, msgs in messages:
                for msg_id, data in msgs:
                    try:
                        print(f"{CONSUMER_NAME} received:", data)

                        # Process
                        from worker.processor import process_event
                        # success = process_event(data)

                        # if success:
                        #     # ACK
                        #     r.xack(STREAM_NAME, GROUP_NAME, msg_id)

                        #     # Optional: mark as completed
                        #     r.hset(f"job:{msg_id}", mapping={
                        #         "status": "completed"
                        #     })
                        print(f"{CONSUMER_NAME} processing:", data)

                        success = process_event(data)

                        if success:
                            r.xack(STREAM_NAME, GROUP_NAME, msg_id)
                            print(f"{CONSUMER_NAME} ACKED message: {msg_id}")

                    except Exception as e:
                        print("Error:", str(e))

                        # Mark failure
                        r.hset(f"job:{msg_id}", mapping={
                            "status": "failed",
                            "error": str(e)
                        })


if __name__ == "__main__":
    worker()