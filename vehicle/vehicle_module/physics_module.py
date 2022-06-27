from data_structures.transform import Transform
from typing import Callable, List


class PhysicsModule:
    transform: Transform
    acceleration_function: Callable[[Transform, List[Transform]], float]

    def __init__(self, **kwargs):
        pass

    def __repr__(self):
        return "PhysicsModule"

    def assemble(self, transform: Transform, **kwargs):
        self.transform = transform
        return self

    def update_position(self, delta_time: float):
        self.transform.position += delta_time * self.transform.velocity
        self.transform.position += (delta_time ** 2) * self.transform.acceleration / 2

    def update_velocity(self, delta_time: float):
        self.transform.velocity += delta_time * self.transform.acceleration

    def update_acceleration(self,
                            acceleration_function: Callable[[Transform, List[Transform]], float],
                            own_data: Transform,
                            distances_list: List[Transform]):
        self.transform.acceleration = acceleration_function(own_data, distances_list)

    def simulate_step(self,
                      acceleration_function: Callable[[Transform, List[Transform]], float],
                      own_data: Transform,
                      distances_list: List[Transform],
                      delta_time):
        self.update_position(delta_time)
        self.update_velocity(delta_time)
        self.update_acceleration(acceleration_function, own_data, distances_list)
