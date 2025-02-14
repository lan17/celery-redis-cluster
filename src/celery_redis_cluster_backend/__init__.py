"""
Celery Redis Cluster Backend
~~~~~~~~~~~~~~~~~~~~~~~~~~~

A Redis Cluster backend implementation for Celery.
"""

from .backend import RedisClusterBackend

__version__ = "0.2.2"


__all__ = ["RedisClusterBackend"]
