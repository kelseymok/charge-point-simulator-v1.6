from unittest.mock import Mock

from event import MessageType

from charge_point import ChargePoint
from unittest import IsolatedAsyncioTestCase

from event_collector import EventCollector
from generator_config import ChargePointConfiguration, ChargePointTransactionConfig
from transactions import Transactions


class TestChargePoint(IsolatedAsyncioTestCase):

    async def test_start(self):
        transactions_storage = Mock(Transactions)
        event_collector = Mock(EventCollector)
        config = ChargePointConfiguration(
            model=f"BB-0",
            vendor="AwEsOmEcHaRgEr",
            on_time="2023-01-01T08:00:00+00:00",
            off_time="2023-01-01T08:20:00+00:00",
            serial_number="e2dd9875-f882-4ca2-8948-e413c456cdf4",
            transactions=[
                ChargePointTransactionConfig(
                    connector=1,
                    start_time="2023-01-01T08:04:00+00:00",
                    stop_time="2023-01-01T08:15:00+00:00",
                )]
        )
        cp = ChargePoint(
            transactions_storage=transactions_storage,
            event_collector=event_collector,
            config=config
        )
        await cp.start()
        assert len(transactions_storage.add_transactions.call_args_list[0][0][0]) == 1
        event_collector_nested_calls = [c[0][0] for c in event_collector.add_events.call_args_list]
        event_collector_calls = [item for sublist in event_collector_nested_calls for item in sublist]
        assert len(event_collector_calls) == 10
        assert [(x.message_type, x.action) for x in event_collector_calls] == [
            (MessageType.request, "BootNotification"),
            (MessageType.successful_response, "BootNotification"),
            (MessageType.request, "HeartBeat"),
            (MessageType.request, "HeartBeat"),
            (MessageType.request, "HeartBeat"),
            (MessageType.request, "HeartBeat"),
            (MessageType.successful_response, "HeartBeat"),
            (MessageType.successful_response, "HeartBeat"),
            (MessageType.successful_response, "HeartBeat"),
            (MessageType.successful_response, "HeartBeat")
        ]

    async def test__beat(self):
        transactions_storage = Mock(Transactions)
        event_collector = Mock(EventCollector)
        config = ChargePointConfiguration(
            model=f"BB-0",
            vendor="AwEsOmEcHaRgEr",
            on_time="2023-01-01T08:00:00+00:00",
            off_time="2023-01-01T08:20:00+00:00",
            serial_number="e2dd9875-f882-4ca2-8948-e413c456cdf4",
            transactions=[
                ChargePointTransactionConfig(
                    connector=1,
                    start_time="2023-01-01T08:04:00+00:00",
                    stop_time="2023-01-01T08:15:00+00:00",
            )]
        )
        cp = ChargePoint(
            transactions_storage=transactions_storage,
            event_collector=event_collector,
            config=config
        )
        await cp._beat("2023-01-01T08:00:00+00:00", "2023-01-01T08:10:00+00:00")
        assert len(event_collector.add_events.call_args_list[0][0][0]) == 2
    async def test__boot(self):
        transactions_storage = Mock(Transactions)
        event_collector = Mock(EventCollector)
        config = ChargePointConfiguration(
            model=f"BB-0",
            vendor="AwEsOmEcHaRgEr",
            on_time="2023-01-01T08:00:00+00:00",
            off_time="2023-01-01T08:20:00+00:00",
            serial_number="e2dd9875-f882-4ca2-8948-e413c456cdf4",
            transactions=[
                ChargePointTransactionConfig(
                    connector=1,
                    start_time="2023-01-01T08:04:00+00:00",
                    stop_time="2023-01-01T08:15:00+00:00",
                )]
        )
        cp = ChargePoint(
            transactions_storage=transactions_storage,
            event_collector=event_collector,
            config=config
        )
        await cp._boot()
        assert len(event_collector.add_events.call_args_list[0][0][0]) == 1


