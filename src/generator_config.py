
from dataclasses import dataclass
from typing import List


@dataclass
class ChargePointTransactionConfig:
    connector: int
    start_time: str
    stop_time: str


@dataclass
class ChargePointConfiguration:
    model: str
    vendor: str
    on_time: str
    off_time: str
    serial_number: str
    transactions: List[ChargePointTransactionConfig]