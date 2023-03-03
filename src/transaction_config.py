from dataclasses import dataclass


@dataclass
class TransactionConfig:
    charge_point_id: str
    connector: int
    start_time: str
    stop_time: str