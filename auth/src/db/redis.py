from redis.asyncio import Redis
from abc import ABC, abstractmethod

redis: Redis | None = None


class AbstractCache(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    async def get(self, key: str) -> str:
        """
        Забрать данные из кеша по ключу
        """
        pass

    @abstractmethod
    async def put(self, key: str, value: str, cache_time: int = None):
        """
        Положить данные в кеш по ключу с временем жизни
        """
        pass

    @abstractmethod
    async def sadd(self, key: str, value: str):
        """
        Положить множество в кеш по ключу
        """
        pass

    @abstractmethod
    async def srem(self, key: str, value: str):
        """
        Удалить элемент множества из кеша по ключу
        """
        pass

    @abstractmethod
    async def smembers(self, key: str) -> set:
        """
        Получение всех элементов множества
        """
        pass

    @abstractmethod
    async def delete(self, key: str) -> set:
        """
        Удаляет по ключу объект из кеша
        """
        pass


class RedisCache(AbstractCache):
    def __init__(self, cache):
        self.cache = cache

    async def get(self, key: str) -> str:
        return await self.cache.get(key)

    async def put(self, key: str, value: str, cache_time: int = None):
        await self.cache.set(key, value, cache_time)
        return await self.cache.get(key)

    async def sadd(self, key: str, value: str):
        await self.cache.sadd(key, value)

    async def srem(self, key: str, value: str):
        await self.cache.srem(key, value)

    async def smembers(self, key: str) -> set:
        return await self.cache.smembers(key)

    async def delete(self, key: str):
        await self.cache.delete(key)

    async def close(self):
        await self.cache.close()


async def get_redis() -> RedisCache:
    return RedisCache(redis)
