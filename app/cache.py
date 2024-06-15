#!/usr/bin/env python3

"""Redis cache implementtion"""

import redis
import uuid
from typing import Union, Callable, Any


class Cache:
    """cache class"""

    def __init__(self) -> None:
        """init redis cache"""

        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, key: str, data: Union[str, bytes, int, float], expires: int = 3600) -> str:
        """store the input data in Redis"""
        self._redis.set(key, data, ex=expires)
        return key

    def get(self, key: str,
            fn: Union[Callable[[bytes], Any], None] = None) -> Any:
        """get data from redis and convert to desired format"""
        data: bytes = self._redis.get(key)
        if data and fn is not None:
            return fn(data)
        return data

    def get_str(self, data: bytes) -> str:
        """convert to str"""
        return data.decode('utf-8')

    def get_int(self, data: bytes) -> int:
        """convert to integer"""
        return int(data)