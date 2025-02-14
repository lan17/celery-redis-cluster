import pytest
from celery import Celery
from pytest import mark
from celery.backends.redis import RedisBackend

from celery_redis_cluster_backend import RedisClusterBackend


# Register the backend
def install_redis_cluster_backend():
    from celery.app.backends import BACKEND_ALIASES

    BACKEND_ALIASES["redis"] = (
        "celery_redis_cluster_backend.backend:choose_redis_backend"
    )
    BACKEND_ALIASES["rediss"] = (
        "celery_redis_cluster_backend.backend:choose_rediss_backend"
    )


@mark.parametrize(
    "protocol, expected_backend",
    [
        ("redis", RedisBackend),
        ("rediss", RedisBackend),
        ("redis+cluster", RedisClusterBackend),
        ("rediss+cluster", RedisClusterBackend),
    ],
)
def test_redis_cluster_backend_installation(protocol, expected_backend):
    install_redis_cluster_backend()

    ssl_options = "?ssl_cert_reqs=CERT_NONE" if "rediss" in protocol else ""

    app = Celery(
        "test_app",
        broker="redis://localhost:6379/0",
        backend=f"{protocol}://localhost:6379{ssl_options}",
    )

    # Check if the backend is set correctly
    assert isinstance(app.backend, expected_backend), (
        "Backend is not set to RedisClusterBackend"
    )


def test_redis_cluster_backend_startup_nodes():
    install_redis_cluster_backend()

    app = Celery(
        "test_app",
        broker="redis://localhost:6379/0",
        backend="redis+cluster://:@localhost:6379",
        redis_max_connections=100,
        redis_socket_timeout=1,
        redis_socket_connect_timeout=1,
        redis_retry_on_timeout=True,
        result_backend_transport_options={
            "startup_nodes": [{"host": "localhost", "port": 6379}],
            "dynamic_startup_nodes": False,
            "username": "foo@bar.com",
            "password": "secret",
        },
    )

    backend = app.backend
    assert isinstance(backend, RedisClusterBackend)

    assert "foo@bar.com" == backend.connparams["username"]
    assert "secret" == backend.connparams["password"]

    assert 1 == len(app.backend.connparams["startup_nodes"])

    assert not app.backend.connparams["dynamic_startup_nodes"]


def test_redis_cluster_backend_no_startup_nodes():
    install_redis_cluster_backend()

    app = Celery(
        "test_app",
        broker="redis://localhost:6379/0",
        backend="redis+cluster://foo:password@localhost:6379",
        redis_max_connections=100,
        redis_socket_timeout=1,
        redis_socket_connect_timeout=1,
        redis_retry_on_timeout=True,
    )

    backend = app.backend
    assert isinstance(backend, RedisClusterBackend)

    assert "foo" == backend.connparams["username"]
    assert "password" == backend.connparams["password"]


if __name__ == "__main__":
    pytest.main()
