import pytest
from celery import Celery

from celery_redis_cluster_backend import RedisClusterBackend, install_redis_cluster_backend

install_redis_cluster_backend()

def test_redis_cluster_backend_installation():
    # Initialize Celery app with RedisClusterBackend
    app = Celery(
        'test_app',
        broker='redis://localhost:6379/0',
        backend='rediscluster://localhost:6379/0'
    )

    # Check if the backend is set correctly
    assert isinstance(app.backend, RedisClusterBackend), "Backend is not set to RedisClusterBackend"

if __name__ == "__main__":
    pytest.main()