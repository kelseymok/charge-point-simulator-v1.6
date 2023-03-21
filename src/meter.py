class Meter:
    def __init__(self):
        self.current_meter = 0

    def increase_meter(self, w_value: int):
        self.current_meter = int(self.current_meter + w_value)
