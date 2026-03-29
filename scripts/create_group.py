from app.redis_client import get_redis
from app.config import STREAM_NAME, GROUP_NAME

r = get_redis()

try:
    r.xgroup_create(STREAM_NAME, GROUP_NAME, id="0", mkstream=True)
    print("Group created")
except Exception:
    print("Group already exists")