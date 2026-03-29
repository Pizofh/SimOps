from enum import Enum


class Severity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    TIMEOUT = "timeout"
    LATENCY_SPIKE = "latency_spike"

