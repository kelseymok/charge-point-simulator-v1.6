import random

from event import MessageType
from generator_config import TransactionConfig, TransactionSessionConfig
from meter import Meter
from transactions import Transactions


class TestTransctions:

    def test_add_transactions(self):
        transactions_storage = Transactions()
        transaction_config_a_meter = Meter()
        transaction_config_a = TransactionConfig(
            charge_point_id="123",
            connector=1,
            start_time="2022-01-01 08:05:00",
            stop_time="2022-01-01 10:15:00",
            sessions=[
                TransactionSessionConfig(
                    start_time="2022-01-01 08:05:00",
                    stop_time="2022-01-01 10:15:00",
                )
            ],
            meter=transaction_config_a_meter
        )

        transaction_config_b_meter = Meter()
        transaction_config_b = TransactionConfig(
            charge_point_id="123",
            connector=1,
            start_time="2022-01-01 13:00:00",
            stop_time="2022-01-01 14:00:00",
            sessions=[
                TransactionSessionConfig(
                    start_time="2022-01-01 13:00:00",
                    stop_time="2022-01-01 13:15:00"
                ),
                TransactionSessionConfig(
                    start_time="2022-01-01 13:30:00",
                    stop_time="2022-01-01 13:45:00"
                )
            ],
            meter=transaction_config_b_meter
        )
        transactions_storage.add_transactions([transaction_config_b, transaction_config_a])

        assert transactions_storage.transactions_list == [
            TransactionConfig(
                charge_point_id="123",
                connector=1,
                start_time="2022-01-01 13:00:00",
                stop_time="2022-01-01 14:00:00",
                sessions=[
                    TransactionSessionConfig(
                        start_time="2022-01-01 13:00:00",
                        stop_time="2022-01-01 13:15:00"
                    ),
                    TransactionSessionConfig(
                        start_time="2022-01-01 13:30:00",
                        stop_time="2022-01-01 13:45:00"
                    )
                ],
                meter=transaction_config_b_meter
            ),
            TransactionConfig(
                charge_point_id="123",
                connector=1,
                start_time="2022-01-01 08:05:00",
                stop_time="2022-01-01 10:15:00",
                sessions=[
                    TransactionSessionConfig(
                        start_time="2022-01-01 08:05:00",
                        stop_time="2022-01-01 10:15:00",
                    )
                ],
                meter=transaction_config_a_meter
            )
        ]

    def test_sort_transactions(self):
        transactions_storage = Transactions()
        transactions_config_a_meter = Meter()
        transaction_config_a = TransactionConfig(
            charge_point_id="123",
            connector=1,
            start_time="2022-01-01 08:05:00",
            stop_time="2022-01-01 10:15:00",
            sessions=[
                TransactionSessionConfig(
                    start_time="2022-01-01 08:05:00",
                    stop_time="2022-01-01 10:15:00",
                )
            ],
            meter=transactions_config_a_meter
        )
        transactions_config_b_meter = Meter()
        transaction_config_b = TransactionConfig(
            charge_point_id="123",
            connector=1,
            start_time="2022-01-01 13:00:00",
            stop_time="2022-01-01 14:00:00",
            sessions=[
                TransactionSessionConfig(
                    start_time="2022-01-01 13:00:00",
                    stop_time="2022-01-01 13:15:00"
                ),
                TransactionSessionConfig(
                    start_time="2022-01-01 13:30:00",
                    stop_time="2022-01-01 13:45:00"
                )
            ],
            meter=transactions_config_b_meter
        )
        transactions_storage.add_transactions([transaction_config_b, transaction_config_a])
        result = transactions_storage.sort_transactions()
        assert result == [
            TransactionConfig(
                charge_point_id="123",
                connector=1,
                start_time="2022-01-01 08:05:00",
                stop_time="2022-01-01 10:15:00",
                sessions=[
                    TransactionSessionConfig(
                        start_time="2022-01-01 08:05:00",
                        stop_time="2022-01-01 10:15:00",
                    )
                ],
                meter=transactions_config_a_meter
            ),
            TransactionConfig(
                charge_point_id="123",
                connector=1,
                start_time="2022-01-01 13:00:00",
                stop_time="2022-01-01 14:00:00",
                sessions=[
                    TransactionSessionConfig(
                        start_time="2022-01-01 13:00:00",
                        stop_time="2022-01-01 13:15:00"
                    ),
                    TransactionSessionConfig(
                        start_time="2022-01-01 13:30:00",
                        stop_time="2022-01-01 13:45:00"
                    )
                ],
                meter=transactions_config_b_meter
            )
        ]

    def test_play_transactions(self):
        random.seed(10)
        transaction_config_a = TransactionConfig(
            charge_point_id="123",
            connector=1,
            start_time="2022-01-01T08:05:00+00:00",
            stop_time="2022-01-01T08:11:00+00:00",
            sessions=[
                TransactionSessionConfig(
                    start_time="2022-01-01T08:05:00+00:00",
                    stop_time="2022-01-01T08:11:00+00:00",
                )
            ],
            meter=Meter()
        )

        transaction_config_b = TransactionConfig(
            charge_point_id="123",
            connector=1,
            start_time="2022-01-01T13:00:00+00:00",
            stop_time="2022-01-01T13:06:00+00:00",
            sessions=[
                TransactionSessionConfig(
                    start_time="2022-01-01T13:00:00+00:00",
                    stop_time="2022-01-01T13:06:00+00:00"
                )
            ],
            meter=Meter()
        )
        transactions_storage = Transactions()
        transactions_storage.add_transactions([transaction_config_b, transaction_config_a])
        transactions_storage.play_transactions()
        result = transactions_storage.played_transactions
        assert len(result) == 2
        last_transaction = result[1]
        assert len(last_transaction) == 16
        assert [(x.message_type, x.action, x.write_timestamp) for x in last_transaction] == [
            (MessageType.request, "StartTransaction", "2022-01-01T13:00:01+00:00"),
            (MessageType.successful_response, "StartTransaction", "2022-01-01T13:00:02+00:00"),
            (MessageType.request, "StatusNotification", "2022-01-01T13:00:03+00:00"),
            (MessageType.successful_response, "StatusNotification", "2022-01-01T13:00:04+00:00"),
            (MessageType.request, "StatusNotification", "2022-01-01T13:00:04+00:00"),
            (MessageType.successful_response, "StatusNotification", "2022-01-01T13:00:05+00:00"),
            (MessageType.request, "MeterValues", "2022-01-01T13:00:06+00:00"),
            (MessageType.request, "MeterValues", "2022-01-01T13:05:06+00:00"),
            (MessageType.successful_response, "MeterValues", "2022-01-01T13:00:07+00:00"),
            (MessageType.successful_response, "MeterValues", "2022-01-01T13:05:07+00:00"),
            (MessageType.request, "StatusNotification", "2022-01-01T13:06:00+00:00"),
            (MessageType.successful_response, "StatusNotification", "2022-01-01T13:06:01+00:00"),
            (MessageType.request, "StopTransaction", "2022-01-01T13:06:00+00:00"),
            (MessageType.successful_response, "StopTransaction", "2022-01-01T13:06:01+00:00"),
            (MessageType.request, "StatusNotification", "2022-01-01T13:06:02+00:00"),
            (MessageType.successful_response, "StatusNotification", "2022-01-01T13:06:03+00:00")
        ]
        assert last_transaction[-4].__dict__["body"]["transaction_id"] == 2
        assert transactions_storage.played is True
