import random

from generator_config import TransactionConfig, TransactionSessionConfig
from transactions import Transactions


class TestTransctions:

    def test_add_transactions(self):
        transactions_storage = Transactions()
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
            ]
        )

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
            ]
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
                ]
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
                ]
            )
        ]

    def test_sort_transactions(self):
        transactions_storage = Transactions()
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
            ]
        )

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
            ]
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
                ]
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
                ]
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
            ]
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
            ]
        )
        transactions_storage = Transactions()
        transactions_storage.add_transactions([transaction_config_b, transaction_config_a])
        transactions_storage.play_transactions()
        result = transactions_storage.played_transactions
        assert len(result) == 2
        last_transaction = result[1]
        assert len(last_transaction) == 6
        assert last_transaction[2].body["transaction_id"] == 2
        assert transactions_storage.played is True
