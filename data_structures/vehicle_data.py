from . import Transform
from typing import List
import math


class VehicleData:
    vehicle_id: int
    transform: Transform
    history: List[Transform]
    vehicle_length: float
    modulo: float

    def __init__(self, vehicle_id: int, transform: Transform, vehicle_length: float, modulo: float = None):
        self.vehicle_id = vehicle_id
        self.transform = transform
        self.history = [transform.copy()]
        self.vehicle_length = vehicle_length
        self.modulo = modulo

    def __str__(self):
        return f"Vehicle {self.vehicle_id}: {self.transform}"

    def __len__(self):
        return len(self.history)

    def age(self):
        return len(self.history)

    def update(self):
        self.history.append(self.transform.wrap(self.modulo).copy())

    def __getitem__(self, n: int):
        return self.history[n]

    def get_at(self, time_step: float) -> Transform:
        time_step = max(min(time_step, len(self) - 1), 0)

        first_value = self[math.floor(time_step)]
        second_value = self[math.ceil(time_step)]
        beta = 1 - time_step % 1

        return first_value.modulo_combination(second_value, self.modulo, beta, 1-beta)

    def distance_at(self, other: "VehicleData", time_step: float):
        no_length_distance = other.get_at(time_step).modulo_combination(self.get_at(time_step), self.modulo, 1, -1)
        return (no_length_distance - Transform(other.vehicle_length, 0, 0)).wrap(self.modulo)
