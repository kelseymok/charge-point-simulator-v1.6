import asyncio
from ocpp.v16 import call, call_result
from ocpp.v16.enums import RegistrationStatus

from event import Event, MessageType
from event_collector import EventCollector
from helpers import pulse
from transaction_config import TransactionConfig
from transactions import Transactions
from generator_config import ChargePointConfiguration
from dateutil import parser
from datetime import timedelta


class ChargePoint:
    def __init__(self,
                 transactions_storage: Transactions,
                 event_collector: EventCollector,
                 config: ChargePointConfiguration):
        self.transactions_storage = transactions_storage
        self.event_collector = event_collector
        self.model = config.model
        self.vendor = config.vendor
        self.serial_number = config.serial_number
        self.on_time = config.on_time
        self.off_time = config.off_time
        self.transactions_config = config.transactions

    async def start(self):
        await asyncio.gather(
            self._boot(),
            self._beat(self.on_time, self.off_time)
        )

        transactions_config = [
            TransactionConfig(
                charge_point_id=self.serial_number,
                connector=t.connector,
                start_time=t.start_time,
                stop_time=t.stop_time
            )
            for t in self.transactions_config
        ]

        self.transactions_storage.add_transactions(transactions_config)

    async def _boot(self):
        action = "BootNotification"
        ending_time = (parser.parse(self.on_time) + timedelta(seconds=1)).isoformat()
        requests, responses = pulse(
            f_request=self._boot_notification_request,
            f_response=self._boot_notification_response,
            starting_time=self.on_time,
            ending_time=ending_time,
            freq=60*5
        )
        self.event_collector.add_events([Event(message_type=MessageType.request, charge_point_id=self.serial_number,
                                               action=action, body=x[0], write_timestamp=x[1]) for x in requests])
        self.event_collector.add_events([Event(message_type=MessageType.successful_response,
                                               charge_point_id=self.serial_number, action=action, body=x[0],
                                               write_timestamp=x[1]) for x in responses])

    async def _beat(self, starting_time, ending_time, freq=60*5):
        requests, responses = pulse(f_request=self._heartbeat_request, f_response=self._heartbeat_response, starting_time=starting_time, ending_time=ending_time, freq=freq)
        self.event_collector.add_events([Event(message_type=MessageType.request, charge_point_id=self.serial_number, action="HeartBeat", body=x[0], write_timestamp=x[1]) for x in requests])
        self.event_collector.add_events([Event(message_type=MessageType.successful_response, charge_point_id=self.serial_number, action="HeartBeat", body=x[0], write_timestamp=x[1]) for x in responses])

    def _boot_notification_request(self, **kwargs):
        return call.BootNotificationPayload(
            charge_point_model=self.model,
            charge_point_vendor=self.vendor,
            charge_point_serial_number=self.serial_number
        ).__dict__

    def _boot_notification_response(self, **kwargs):
        return call_result.BootNotificationPayload(
            current_time=kwargs["now"],
            interval=300,
            status=RegistrationStatus.accepted
        ).__dict__

    def _heartbeat_request(self, **kwargs):
        return call.HeartbeatPayload().__dict__

    def _heartbeat_response(self, **kwargs):
        return call_result.HeartbeatPayload(current_time=kwargs["now"])