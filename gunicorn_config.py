import os

# Use Render's PORT environment variable, default to 10000
port = os.environ.get("PORT", "10000")
bind = f"0.0.0.0:{port}"

# Worker configuration
workers = 2
threads = 4
timeout = 120

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Prevent early timeouts
keepalive = 5
