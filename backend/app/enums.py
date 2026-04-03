from enum import StrEnum


class Severity(StrEnum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    TIMEOUT = "timeout"
    LATENCY_SPIKE = "latency_spike"

