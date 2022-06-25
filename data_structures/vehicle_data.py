import math
from typing import List
from .transform import Transform


class VehicleData:
    vehicle_id: int
    transform: Transform
    position: List[float]
    velocity: List[float]
    acceleration: List[float]
    length: float

    def __init__(self, transform, vehicle_id):
        self.vehicle_id = vehicle_id
        self.transform = transform
        self.position = [transform.position]
        self.velocity = [transform.velocity]
        self.acceleration = [transform.acceleration]
        self.length = transform.length

    def __str__(self):
        return f"{str(self.position)}; {str(self.velocity)}; {str(self.acceleration)}; {str(self.length)}"

    def __len__(self):
        if len(self.position) == len(self.velocity) and len(self.position) == len(self.acceleration):
            return len(self.position)
        raise ValueError()

    def get_at(self, i, modulo=None):
        if i > len(self) - 1 or i == -1:
            return self.get_at(len(self)-1)
        if i < 0:
            return self.get_at(0)
        if type(i) == int:
            return Transform(self.position[i], self.velocity[i], self.acceleration[i], self.length)
        if type(i) == float:
            beta = 1 - i % 1
            if modulo is None:
                return self.get_at(math.floor(i)) * beta + self.get_at(math.ceil(i)) * (1 - beta)

            value_before = self.get_at(math.floor(i))
            value_after = self.get_at(math.ceil(i))

            if (value_before.position > (modulo * 2/3)) and (value_after.position < (modulo * 1/3)):
                # passed the modulo wrap
                value_after.position += modulo
            elif (value_before.position < (modulo * 1/3)) and (value_after.position > (modulo * 2/3)):
                # reverse passed the modulo wrap
                value_before.position += modulo

            value = (value_before * beta + value_after * (1 - beta))
            value.position = value.position % modulo
            return value

    def update(self):
        self.position.append(self.transform.position)
        self.velocity.append(self.transform.velocity)
        self.acceleration.append(self.transform.acceleration)
