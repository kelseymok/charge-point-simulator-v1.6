import json
from typing import Dict
from dateutil import parser


class Event:
    def __init__(self, charge_point_id: str, action: str, body: Dict, write_timestamp: str):
        self.charge_point_id = charge_point_id
        self.action = action
        self.body = body
        self.write_timestamp = write_timestamp

    def format(self):
        return {
            "charge_point_id": self.charge_point_id,
            "action": self.action,
            "write_timestamp": parser.parse(self.write_timestamp).isoformat(),
            "body": json.dumps(self.body)
        }