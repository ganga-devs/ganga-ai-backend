import redis
import uuid
from root.settings import environment_variables
from redis.client import Redis

redis_client = redis.Redis(
    db=environment_variables["REDIS_DB"],
    host=environment_variables["REDIS_HOST"],
    port=environment_variables["REDIS_PORT"],
    # Ensures strings are returned instead of bytes
    decode_responses=True
)


def get_or_create_user_uuid(user_id: str) -> str:
    key = f"user_map:{user_id}"
    user_uuid = redis_client.get(key)
    if user_uuid:
        return user_uuid
    user_uuid = str(uuid.uuid4())
    redis_client.set(key, user_uuid)
    return user_uuid


def store_message(user_uuid: str, role: str, message: str):
    key = f"history:{user_uuid}"
    redis_client.rpush(key, f"{role}:{message}")
    redis_client.ltrim(key, -50, -1)

def get_conversation_history(user_uuid: str, limit: int = 10):
    key = f"history:{user_uuid}"
    messages = redis_client.lrange(key, -limit, -1)
    return [tuple(m.split(":", 1)) for m in messages]

def clear_conversation_history(user_uuid: str):
    redis_client.delete(f"history:{user_uuid}")
