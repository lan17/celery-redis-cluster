# Celery Redis Cluster

A Redis Cluster backend implementation for Celery. This package extends Celery's Redis backend to work with Redis Cluster, providing better scalability and high availability through Redis Cluster's sharding and replication capabilities.

## Installation

```bash
pip install celery-redis-cluster
```

After installation new backends are automatically registered with Celery:
- `redis+cluster`
- `rediss+cluster`

## Usage

To use the Redis Cluster backend in your Celery application:

```python
from celery import Celery

from celery_redis_cluster_backend import install_redis_cluster_backend

# Registers with celery backends
install_redis_cluster_backend()

app = Celery('your_app',
             broker='redis://localhost:6379/0',
             backend='redis+cluster://localhost:6379/0')
```

### Configuration

The backend inherits all configuration options from Celery's Redis backend, with the addition of Redis Cluster specific handling. Here's an example configuration:

```python
app.conf.update(
    result_backend='redis+cluster://localhost:6379/0',
    redis_backend_use_ssl={
        'ssl_cert_reqs': None,
        'ssl_ca_certs': None,
        'ssl_certfile': None,
        'ssl_keyfile': None
    },
    redis_max_connections=None,
    redis_socket_timeout=120.0,
    redis_socket_connect_timeout=120.0,
    redis_cluster_retry_on_timeout=True,
    redis_cluster_max_retry_on_timeout=3,
)
```

## Requirements

- Python >= 3.8
- Celery >= 5.3.0
- redis >= 4.5.0

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
