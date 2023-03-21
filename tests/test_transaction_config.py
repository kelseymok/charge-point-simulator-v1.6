from generator_config import TransactionConfig, TransactionSessionConfig
from meter import Meter


class TestTransactionConfig:
    def test_transaction_config(self):
        config = {
            "charge_point_id": "123",
            "connector": 1,
            "start_time": "2022-01-01 08:05:00",
            "stop_time": "2022-01-01 10:15:00",
            "sessions": [
                TransactionSessionConfig(
                    start_time="2022-01-01 08:05:00",
                    stop_time="2022-01-01 10:15:00",
                )
            ],
            "meter": Meter()
        }

        result = TransactionConfig(**config)

        assert result.charge_point_id == "123"
        assert result.connector == 1
        assert result.start_time == "2022-01-01 08:05:00"
        assert result.stop_time == "2022-01-01 10:15:00"
        assert result.meter.current_meter == 0
