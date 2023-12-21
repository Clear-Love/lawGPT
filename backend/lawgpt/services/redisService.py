import redis
from redis import ConnectionPool
from lawgpt.config import settings

class RedisClient:
    def __init__(self, host=settings.REDIS.HOST, port=settings.REDIS.PORT, db=0, max_connections=settings.REDIS.MAX_CONNECTIONS):
        pool = ConnectionPool(host=host, port=port, db=db,
                              max_connections=max_connections)
        self.redis = redis.Redis(connection_pool=pool)

    def set(self, key, value, expire=None):
        self.redis.set(key, value)
        if expire:
            self.redis.expire(key, expire)

    def get(self, key):
        return self.redis.get(key)

    def get_str(self, key):
        result = self.redis.get(key)
        if result:
            return result.decode()  # 将字节序列转换为字符串
        return None

    def delete(self, key):
        self.redis.delete(key)

    def exists(self, key):
        return self.redis.exists(key)

    def ttl(self, key):
        return self.redis.ttl(key)


if __name__ == '__main__':
    # 示例用法
    redis_client = RedisClient()
    redis_client.set('name', 'John')
    value = redis_client.get('name')
    print(value)  # 输出: b'John'
