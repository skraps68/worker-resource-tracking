"""Data models for Worker and Resource."""
from datetime import datetime, date
from dataclasses import dataclass


# Infinity constants
INFINITY_DATE = date(9999, 12, 31)
INFINITY_DATETIME = datetime(9999, 12, 31, 23, 59, 0)


@dataclass
class Worker:
    """Worker model."""
    WID: int
    name: str
    org: str
    type: str


@dataclass
class Resource:
    """Resource model."""
    RID: int
    version: int
    WID: int
    res_start: date
    res_end: date
    proc_start: datetime
    proc_end: datetime


@dataclass
class ResourceWithWorker:
    """Resource with worker information for display."""
    RID: int
    version: int
    WID: int
    name: str
    org: str
    type: str
    res_start: date
    res_end: date
    proc_start: datetime
    proc_end: datetime
