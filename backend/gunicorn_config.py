# Gunicorn configuration for production
import multiprocessing
import os

# Server socket
bind = f"0.0.0.0:{os.environ.get('PORT', 5000)}"
backlog = 2048

# Worker processes
workers = 1  # Reduced for memory constraints on free tier
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Process naming
proc_name = 'hospital_management_system'

# SSL (if needed, uncomment and provide paths)
# keyfile = "/etc/ssl/private/key.pem"
# certfile = "/etc/ssl/certs/cert.pem"

# Server hooks
def on_starting(server):
    print("Gunicorn server starting...")

def when_ready(server):
    print("Gunicorn server is ready. Spawning workers")

def on_exit(server):
    print("Gunicorn server exiting")
