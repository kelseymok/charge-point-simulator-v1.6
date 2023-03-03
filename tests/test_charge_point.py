from charge_point import ChargePoint
from unittest import IsolatedAsyncioTestCase

class TestChargePoint(IsolatedAsyncioTestCase):
    async def test_beat(self):
        cp = ChargePoint(meter={})
        await cp._beat("2022-01-01 08:00:00", "2022-01-01 09:00:00")

    async def test_boot(self):
        cp = ChargePoint(meter={})
        await cp._boot("2022-01-01 08:00:00")

    async def test_start(self):
        cp = ChargePoint(
            meter={},
            starting_time="2022-01-01 08:00:00",
            ending_time="2022-01-01 09:00:00")
        await cp.start()

