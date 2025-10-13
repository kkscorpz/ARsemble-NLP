import os
import multiprocessing

bind = "0.0.0.0:" + os.environ.get("PORT", "10000")
workers = 1
worker_class = "sync"
timeout = 300  # Increase timeout to 5 minutes
max_requests = 1000
max_requests_jitter = 100
preload_app = True  # Preload app to reduce memory usage
