"""Redis Cluster backend for Celery."""

import functools
from copy import copy
from typing import Any

from celery.backends.redis import RedisBackend
from redis.cluster import RedisCluster, ClusterNode
from redis.exceptions import RedisClusterException


def choose_backend(scheme, *args, **kwargs):
    url = kwargs.get("url", "")

    def patch_url(additional):
        nonlocal url
        kwargs["url"] = url.replace(additional, scheme, 1)

    if url.startswith("cluster"):
        patch_url("cluster")
        return RedisClusterBackend(*args, **kwargs)
    else:
        return RedisBackend(*args, **kwargs)


def choose_redis_backend(*args, **kwargs):
    return choose_backend("redis", *args, **kwargs)


def choose_rediss_backend(*args, **kwargs):
    return choose_backend("rediss", *args, **kwargs)


class RedisClusterBackend(RedisBackend):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

        # Add RedisClusterException to the list of connection errors since
        # its not there by default
        self.connection_errors = (RedisClusterException,) + self.connection_errors  # type: ignore[has-type]

        # RedisCluster uses its own connection pool, so we just create a singleton connection here
        # and return it when client is requested.
        del self.connparams["db"]  # RedisCluster does not take in 'db' param
        if "app" in kwargs:
            # Try to get startup_nodes if present in app config.
            transport_options = copy(
                kwargs["app"].conf.get("result_backend_transport_options", {})
            )
            self.connparams["startup_nodes"] = transport_options.get(
                "startup_nodes", None
            )
            if self.connparams["startup_nodes"]:
                self.connparams["startup_nodes"] = [
                    ClusterNode(**node) for node in self.connparams["startup_nodes"]
                ]

            # Remove startup nodes from transport options so that we can just pass rest of transport options to connparams
            try:
                del transport_options["startup_nodes"]
            except KeyError:
                pass

            # Dump rest of transport_options directly into the connparams
            self.connparams.update(transport_options)
        else:
            self.startup_nodes = None

    @functools.lru_cache
    def create_redis_cluster(self) -> RedisCluster:
        return RedisCluster(**self.connparams)  # type: ignore[abstract]

    def _create_client(self, **params: Any) -> RedisCluster:
        return self.create_redis_cluster()
