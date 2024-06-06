import redis
# from config import REDIS_HOST, REDIS_DB, REDIS_PORT

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0


try:
    redis_connect = redis.Redis(REDIS_HOST, REDIS_PORT, REDIS_DB)
    redis_connect.set('my_key', 'my_value')
    value = redis_connect.get('my_key')
except redis.exceptions.ConnectionError as e:
    print(f"Error connecting to Redis: {e}")
