
from dataclasses import dataclass
from typing import List


@dataclass
class TransactionSessionConfig:
    start_time: str
    stop_time: str


@dataclass
class TransactionConfig:
    charge_point_id: str
    connector: int
    start_time: str
    stop_time: str
    sessions: List[TransactionSessionConfig]


@dataclass
class ChargePointTransactionConfig:
    connector: int
    start_time: str
    stop_time: str
    sessions: List[TransactionSessionConfig]


@dataclass
class ChargePointConfiguration:
    model: str
    vendor: str
    on_time: str
    off_time: str
    serial_number: str
    transactions: List[ChargePointTransactionConfig]

