"""
Celery Redis Cluster Backend
~~~~~~~~~~~~~~~~~~~~~~~~~~~

A Redis Cluster backend implementation for Celery.
"""

from .backend import RedisClusterBackend

__version__ = "0.1.9"


__all__ = ["RedisClusterBackend"]
