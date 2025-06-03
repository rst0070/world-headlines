import logging
import queue
from logging.handlers import QueueHandler, QueueListener


def init_logging(
    level: str = "INFO",
    handlers: list[logging.Handler] = [],
) -> None:
    """
    Set up logging configuration with queue handler.

    Args:
        level: Logging level (default: "INFO")
    """
    # Create queue
    log_queue = queue.Queue()

    # Get root logger
    root = logging.getLogger()
    root.setLevel(level)

    # Create queue handler and add it to root logger
    queue_handler = QueueHandler(log_queue)
    # queue_handler.setFormatter(JSONFormatter())
    root.addHandler(queue_handler)

    # Create and start queue listener
    listener = QueueListener(log_queue, *handlers, respect_handler_level=True)
    listener.start()

    root.listener = listener


def shutdown_logging() -> None:
    """
    Properly shutdown logging system.
    Should be called when the application exits.
    """
    root = logging.getLogger()
    if hasattr(root, "listener"):
        root.listener.stop()  # type: ignore
