"""Redis Cluster backend for Celery."""

from celery.backends.base import KeyValueStoreBackend
from celery.exceptions import ImproperlyConfigured
from redis.cluster import RedisCluster
from urllib.parse import urlparse
from redis.exceptions import RedisClusterException
import functools
from typing import Any


class RedisClusterBackend(RedisBackend):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

        # Add RedisClusterException to the list of connection errors since
        # its not there by default
        self.connection_errors = (RedisClusterException,) + self.connection_errors  # type: ignore[has-type]

        # RedisCluster uses its own connection pool, so we just create a singleton connection here
        # and return it when client is requested.
        del self.connparams["db"]  # RedisCluster does not take in 'db' param

    @functools.lru_cache
    def create_redis_cluster(self) -> RedisCluster:
        return RedisCluster(**self.connparams)  # type: ignore[abstract]

    def _create_client(self, **params: Any) -> RedisCluster:
        return self.create_redis_cluster()
