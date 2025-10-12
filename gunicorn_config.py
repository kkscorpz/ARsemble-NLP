import os

bind = "0.0.0.0:" + os.environ.get("PORT", "10000")
workers = 1
worker_class = "sync"
worker_connections = 1000
timeout = 120
keepalive = 2
