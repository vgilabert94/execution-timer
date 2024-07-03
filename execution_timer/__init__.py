from __future__ import annotations

__version__ = "0.1.2"

# __init__.py
import execution_timer
from .execution_timer import ExecutionTimer, time_execution

__all__ = ["execution_timer", "ExecutionTimer", "time_execution"]
