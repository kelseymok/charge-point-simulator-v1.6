from meter import Meter


class TestMeter:
    def test_increase_value(self):
        meter = Meter()
        assert meter.current_meter == 0
        meter.increase_meter(1000)
        assert meter.current_meter == 1000
        meter.increase_meter(1000)
        assert meter.current_meter == 2000

    def test_increase_value_returns_int(self):
        meter = Meter()
        assert meter.current_meter == 0
        meter.increase_meter(1000)
        assert meter.current_meter == 1000
        meter.increase_meter(2050.2523)
        assert meter.current_meter == 3050
