from typing import Union
import math


class Transform:
    position: float
    velocity: float

    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity


class Vehicle:
    transform: Transform
    current_acceleration: float
    vehicle_before: Union["Vehicle", None]

    def __init__(self, position, velocity, vehicle_before=None):
        self.transform = Transform(position, velocity)
        self.vehicle_before = vehicle_before
        self.current_acceleration = 0

    def distance(self, other, modulo: float = None):
        dist = other.transform.position - self.transform.position
        if modulo is not None:
            dist = dist % modulo
        return dist

    def update_position(self, delta_time, modulo: float = None):
        self.transform.position += self.transform.velocity * delta_time
        if modulo is not None:
            self.transform.position = self.transform.position % modulo

    def update_velocity(self, delta_time, modulo: float = None):
        self.transform.velocity += self.acceleration(modulo) * delta_time

    def acceleration(self, *args, **kwargs) -> float:
        raise NotImplementedError()

    def simulate_step(self, delta_time, modulo: float = None):
        self.update_velocity(delta_time, modulo)
        self.update_position(delta_time, modulo)


class TestVehicle(Vehicle):

    def __init__(self, position, velocity, vehicle_before=None):
        super(TestVehicle,  self).__init__(position, velocity, vehicle_before)

    def acceleration(self) -> float:
        if self.vehicle_before is None or self.distance(self.vehicle_before) > 5:
            return 1
        else:
            return self.distance(self.vehicle_before)/5


class IDV(Vehicle):
    minimum_distance: float
    max_velocity: float
    max_acceleration: float
    headway_time: float
    comfortable_deceleration: float

    def __init__(self, position, velocity, max_velocity, max_acceleration,
                 minimum_distance, headway_time, comfortable_deceleration):
        self.max_velocity = max_velocity
        self.max_acceleration = max_acceleration
        self.minimum_distance = minimum_distance
        self.headway_time = headway_time
        self.comfortable_deceleration = comfortable_deceleration
        super(IDV, self).__init__(position, velocity)

    def calculate_free_acceleration(self):
        return self.max_acceleration * (1 - (self.transform.velocity / self.max_velocity) ** 4)

    def calculate_desired_minimum_gap(self):
        if self.vehicle_before is None:
            return 0
        return self.minimum_distance + self.vehicle_before.transform.velocity * self.headway_time + \
            self.transform.velocity * (self.transform.velocity - self.vehicle_before.transform.velocity) / \
            math.sqrt(self.max_acceleration * self.comfortable_deceleration)

    def calculate_braking_interaction(self, modulo: float = None):
        return -(self.max_acceleration *
                 (self.calculate_desired_minimum_gap() / self.distance(self.vehicle_before, modulo)) ** 2)

    def acceleration(self, modulo: float = None):
        self.current_acceleration = self.calculate_free_acceleration() + self.calculate_braking_interaction(modulo)

        return self.current_acceleration
