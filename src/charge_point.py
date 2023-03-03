import asyncio
from ocpp.v16 import call

from event import Event
from event_collector import EventCollector
from helpers import pulse
from transaction_config import TransactionConfig
from transactions import Transactions
from generator_config import ChargePointConfiguration


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
        boot = self._boot_notification()
        self.event_collector.add_events([
            Event(
                charge_point_id=self.serial_number,
                action="BootNotification",
                body=boot,
                write_timestamp=self.on_time
            )
        ])

    async def _beat(self, starting_time, ending_time, freq=60*5):
        beats = pulse(f=self._heartbeat, starting_time=starting_time, ending_time=ending_time, freq=freq)
        self.event_collector.add_events([Event(charge_point_id=self.serial_number, action="HeartBeat", body=x[0], write_timestamp=x[1]) for x in beats])

    def _boot_notification(self, **kwargs):
        return call.BootNotificationPayload(
            charge_point_model=self.model,
            charge_point_vendor=self.vendor,
            charge_point_serial_number=self.serial_number
        ).__dict__

    def _heartbeat(self, **kwargs):
        return call.HeartbeatPayload().__dict__