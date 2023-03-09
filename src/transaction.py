import uuid
import random
from datetime import timedelta

from attr import asdict

from event import Event, MessageType
from helpers import pulse

from ocpp.v16 import call, call_result
from ocpp.v16.datatypes import SampledValue, MeterValue, IdTagInfo
from ocpp.v16.enums import ReadingContext, ValueFormat, Measurand, Phase, UnitOfMeasure, AuthorizationStatus
import json
from dateutil import parser
from dateutil.relativedelta import *


class Transaction:
    def __init__(self, id: int, connector: int, charge_point_id: str, start_time: str, stop_time: str, id_tag: str=str(uuid.uuid4())):
        self.charge_point_id = charge_point_id
        self.connector = connector
        self.transaction_id = id
        self.meter_start = 0
        self.meter_current = 0
        self.meter_stop = self.meter_current
        self.start_time = start_time
        self.stop_time = stop_time
        self.id_tag = id_tag

    def start(self):
        collect = self._start()
        collect = collect + self._meter_values_pulse()
        collect = collect + self._stop()

        return collect

    def _increase_meter(self, **kwargs):
        self.meter_current = self.meter_current + kwargs["power_import"]
        return self.meter_current

    def _start(self):
        action = "StartTransaction"
        requests, responses = pulse(
            f_request=self._start_transaction_request,
            f_response=self._start_transaction_response,
            starting_time=self.start_time,
            ending_time=(parser.parse(self.start_time) + timedelta(seconds=1)).isoformat(),
            connector_id=self.connector,
            transaction_id=self.transaction_id,
            power_import=float(random.randint(1330, 1800)),
        )
        collect = []
        collect = collect + [
            Event(message_type=MessageType.request, charge_point_id=self.charge_point_id, action=action, body=x[0],
                  write_timestamp=x[1]) for x in requests]
        collect = collect + [
            Event(message_type=MessageType.successful_response, charge_point_id=self.charge_point_id, action=action,
                  body=x[0], write_timestamp=x[1]) for x in responses]

        return collect

    def _stop(self):
        action = "StopTransaction"
        requests, responses = pulse(
            f_request=self._stop_transaction_request,
            f_response=self._stop_transaction_response,
            starting_time=self.stop_time,
            ending_time=(parser.parse(self.stop_time) + timedelta(minutes=1)).isoformat(),
            connector_id=self.connector,
            transaction_id=self.transaction_id,
            power_import=float(random.randint(1330, 1800)),
        )

        collect = []
        collect = collect + [Event(message_type=MessageType.request, charge_point_id=self.charge_point_id, action=action, body=x[0], write_timestamp=x[1]) for x in requests]
        collect = collect + [Event(message_type=MessageType.successful_response, charge_point_id=self.charge_point_id, action=action, body=x[0], write_timestamp=x[1]) for x in responses]

        return collect

    def _meter_values_pulse(self):
        action = "MeterValues"
        requests, responses = pulse(
                f_request=self._meter_values_request,
                f_response=self._meter_values_response,
                starting_time=(parser.parse(self.start_time) + relativedelta(minutes=+1)).isoformat(),
                ending_time=self.stop_time,
                connector_id=self.connector,
                transaction_id=self.transaction_id,
                power_import=float(random.randint(1330, 1800)),
            )
        collect = []
        collect = collect + [Event(message_type=MessageType.request, charge_point_id=self.charge_point_id, action=action, body=v[0], write_timestamp=v[1]) for v in requests]
        collect = collect + [Event(message_type=MessageType.successful_response, charge_point_id=self.charge_point_id, action=action, body=v[0], write_timestamp=v[1]) for v in responses]
        return collect

    def _start_transaction_request(self, **kwargs):
        return call.StartTransactionPayload(
            connector_id=self.connector,
            id_tag=self.id_tag,
            meter_start=self.meter_start,
            timestamp=self.start_time
        ).__dict__

    def _start_transaction_response(self, **kwargs):
        return call_result.StartTransactionPayload(
            id_tag_info=IdTagInfo(parent_id_tag=self.id_tag, status=AuthorizationStatus.accepted).__dict__,
            transaction_id=self.transaction_id
        ).__dict__

    def _stop_transaction_request(self, **kwargs):
        return call.StopTransactionPayload(
            timestamp=self.stop_time,
            meter_stop=self.meter_stop,
            transaction_id=self.transaction_id,
            id_tag=self.id_tag,
        ).__dict__

    def _stop_transaction_response(self, **kwargs):
        return call_result.StopTransactionPayload(
            id_tag_info=IdTagInfo(parent_id_tag=self.id_tag, status=AuthorizationStatus.accepted).__dict__,
        ).__dict__

    def _add_noise(self, noise_range: float, base: float) -> float:
        noise = random.uniform(noise_range*-1, noise_range)
        return round(base + noise, 2)

    def _meter_values_request(self, **kwargs):
        noisy_power_import = self._add_noise(20.0, kwargs["power_import"])
        noisy_current_import = self._add_noise(2.0, 6.0)
        sampled_values = [
            SampledValue(
                context=ReadingContext.sample_periodic,
                format=ValueFormat.raw,
                measurand=Measurand.voltage,
                phase=Phase.l1_n,
                unit=UnitOfMeasure.v,
                value=str(0.00),
            ),
            SampledValue(
                context=ReadingContext.sample_periodic,
                format=ValueFormat.raw,
                measurand=Measurand.current_import,
                phase=Phase.l1,
                unit=UnitOfMeasure.a,
                value=str(noisy_current_import),
            ),
            SampledValue(
                context=ReadingContext.sample_periodic,
                format=ValueFormat.raw,
                measurand=Measurand.power_active_import,
                phase=Phase.l1,
                unit=UnitOfMeasure.w,
                value=str(noisy_power_import),
            ),
            SampledValue(
                context=ReadingContext.sample_periodic,
                format=ValueFormat.raw,
                measurand=Measurand.voltage,
                phase=Phase.l2_n,
                unit=UnitOfMeasure.v,
                value=str(0.0),
            ),
            SampledValue(
                context=ReadingContext.sample_periodic,
                format=ValueFormat.raw,
                measurand=Measurand.current_import,
                phase=Phase.l2,
                unit=UnitOfMeasure.a,
                value=str(0.0),
            ),
            SampledValue(
                context=ReadingContext.sample_periodic,
                format=ValueFormat.raw,
                measurand=Measurand.power_active_import,
                phase=Phase.l2,
                unit=UnitOfMeasure.w,
                value=str(0.0),
            ),
            SampledValue(
                context=ReadingContext.sample_periodic,
                format=ValueFormat.raw,
                measurand=Measurand.voltage,
                phase=Phase.l3_n,
                unit=UnitOfMeasure.v,
                value=str(0.0),
            ),
            SampledValue(
                context=ReadingContext.sample_periodic,
                format=ValueFormat.raw,
                measurand=Measurand.current_import,
                phase=Phase.l3,
                unit=UnitOfMeasure.a,
                value=str(0.0),
            ),
            SampledValue(
                context=ReadingContext.sample_periodic,
                format=ValueFormat.raw,
                measurand=Measurand.power_active_import,
                phase=Phase.l3,
                unit=UnitOfMeasure.w,
                value=str(0.0),
            ),
            SampledValue(
                context=ReadingContext.sample_periodic,
                format=ValueFormat.raw,
                measurand=Measurand.energy_active_import_register,
                unit=UnitOfMeasure.wh,
                value=str(self._increase_meter(power_import=float(noisy_power_import)))
            ),
            SampledValue(
                value=str(noisy_current_import),
                context=ReadingContext.sample_periodic,
                format=ValueFormat.raw,
                measurand=Measurand.current_import,
                unit=UnitOfMeasure.a
            ),
            SampledValue(
                value=str(noisy_power_import),
                context=ReadingContext.sample_periodic,
                format=ValueFormat.raw,
                measurand=Measurand.power_active_import,
                unit=UnitOfMeasure.w,
            ),
        ]

        meter_value = MeterValue(
            timestamp=kwargs["timestamp"],
            sampled_value=[json.loads(json.dumps(v.__dict__)) for v in sampled_values]
        )

        meter_values = call.MeterValuesPayload(
            connector_id=kwargs["connector_id"],
            transaction_id=kwargs["transaction_id"],
            meter_value=[json.loads(json.dumps(meter_value.__dict__))]
        ).__dict__
        return meter_values

    def _meter_values_response(self, **kwargs):
        return call_result.MeterValuesPayload().__dict__