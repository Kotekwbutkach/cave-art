from data_structures.transform import Transform
from typing import Callable


class Physics:
    transform: Transform

    def __init__(self, position: float, velocity: float, acceleration: float, length: float,
                 **kwargs):
        self.transform = Transform(position, velocity, acceleration, length)

    def update_position(self, delta_time: float):
        self.transform.position += delta_time * self.transform.velocity
        self.transform.position += (delta_time ** 2) * self.transform.acceleration / 2

    def update_velocity(self, delta_time: float):
        self.transform.velocity += delta_time * self.transform.acceleration

    def update_acceleration(self, acceleration_function: Callable):
        self.transform.acceleration = acceleration_function()

    def simulate_step(self, acceleration_function, delta_time):
        self.update_acceleration(acceleration_function)
        self.update_velocity(delta_time)
        self.update_position(delta_time)
