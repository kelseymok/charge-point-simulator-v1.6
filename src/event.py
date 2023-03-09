import json
from enum import Enum
from typing import Dict
from dateutil import parser



class MessageType(int, Enum):
    request = 2
    successful_response = 3
    erroneous_response = 4


class Event:
    def __init__(self, message_type: MessageType, charge_point_id: str, action: str, body: Dict, write_timestamp: str):
        self.message_type = message_type
        self.charge_point_id = charge_point_id
        self.action = action
        self.body = body
        self.write_timestamp = write_timestamp

    def format(self):
        try:
            data = {
                "message_type": self.message_type,
                "charge_point_id": self.charge_point_id,
                "action": self.action,
                "write_timestamp": parser.parse(self.write_timestamp).isoformat(),
                "body": json.dumps(self.body)
            }
            return data

        except Exception as e:
            print(self.body)
            print(e)


