import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load Gunicorn timeout settings from environment variables
timeout = int(os.getenv("GUNICORN_TIMEOUT", 120))
graceful_timeout = int(os.getenv("GUNICORN_GRACEFUL_TIMEOUT", 120))

def worker_exit(server, worker):
    """
    Hook to log when a worker exits.
    """
    logging.warning(f"Worker {worker.pid} exited. Gunicorn will attempt to restart it.")

def worker_abort(worker):
    """
    Hook to handle worker aborts gracefully.
    """
    logging.error(f"Worker {worker.pid} aborted unexpectedly. Gunicorn will restart it if possible.")

def post_request(worker, req, environ, resp):
    """
    Hook to handle post-request logging.
    """
    if req is None:
        logging.warning(f"Worker {worker.pid} received an invalid or incomplete request.")

def worker_timeout(worker):
    """
    Hook to log worker timeout events.
    """
    logging.error(f"Worker {worker.pid} timed out.")