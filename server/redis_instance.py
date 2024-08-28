import redis
from .config import redis_host, redis_port

r = redis.Redis(host=redis_host, port=redis_port)
