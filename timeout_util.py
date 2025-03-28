"""
Timeout utility for TIA Portal MCP Server.

This module provides cross-platform timeout functionality since
the signal.SIGALRM method only works on Unix/Linux.
"""

import threading
import _thread
import time
from contextlib import contextmanager

class TimeoutException(Exception):
    """Exception raised when an operation times out."""
    pass

@contextmanager
def timeout(seconds):
    """
    Context manager that provides timeout functionality on Windows.
    
    Args:
        seconds: Number of seconds to wait before timing out
    
    Raises:
        TimeoutException: If the operation times out
    """
    timer = threading.Timer(seconds, lambda: _thread.interrupt_main())
    timer.start()
    try:
        yield
    except KeyboardInterrupt:
        raise TimeoutException(f"Operation timed out after {seconds} seconds")
    finally:
        timer.cancel()
