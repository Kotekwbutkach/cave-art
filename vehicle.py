from typing import Union
from data_structures import TransformData
from transform import Transform
from wiener import Wiener
import math


class Vehicle:
    transform: Transform
    vehicle_before: Union["Vehicle", None]
    history: TransformData

    def __init__(self, position, velocity, acceleration, vehicle_before=None):
        self.transform = Transform(position, velocity, acceleration)
        self.vehicle_before = vehicle_before
        self.history = TransformData(self.transform)

    def get_net_distance(self, other: "Vehicle", modulo: float, time: float = None):
        return self.transform.distance(other.transform, modulo)

    def get_velocity_difference(self, other: "Vehicle", modulo: float, time: float = None):
        return self.transform.velocity_difference(other.transform)

    def update_position(self, delta_time, modulo: float = None):
        self.transform.position += self.transform.velocity * delta_time +\
                                   self.transform.acceleration * (delta_time**2)/2
        if modulo is not None:
            self.transform.position = self.transform.position % modulo

    def update_velocity(self, delta_time, modulo: float = None):
        self.transform.velocity += self.transform.acceleration * delta_time

    def update_acceleration(self, delta_time, modulo: float = None):
        raise NotImplementedError()

    def simulate_step(self, delta_time, modulo: float = None):
        self.update_acceleration(delta_time, modulo)
        self.update_velocity(delta_time, modulo)
        self.update_position(delta_time, modulo)


class IDV(Vehicle):
    max_velocity: float
    max_acceleration: float
    minimum_distance: float
    headway_time: float
    comfortable_deceleration: float

    def __init__(self, *, position, velocity, acceleration, max_velocity, max_acceleration,
                 minimum_distance, headway_time, comfortable_deceleration):
        self.max_velocity = max_velocity
        self.max_acceleration = max_acceleration
        self.minimum_distance = minimum_distance
        self.headway_time = headway_time
        self.comfortable_deceleration = comfortable_deceleration
        super(IDV, self).__init__(position, velocity, acceleration)

    def calculate_free_acceleration(self):
        return self.max_acceleration * (1 - (self.transform.velocity / self.max_velocity) ** 4)

    def calculate_desired_minimum_gap(self, other: "Vehicle", modulo: float):
        return self.minimum_distance + self.transform.velocity * self.headway_time + \
            self.transform.velocity * self.get_velocity_difference(other, modulo) / \
            2 * math.sqrt(self.max_acceleration * self.comfortable_deceleration)

    def calculate_braking_interaction(self, other: "Vehicle", modulo: float):
        return -(self.max_acceleration *
                 (self.calculate_desired_minimum_gap(other, modulo) / self.get_net_distance(other, modulo)) ** 2)

    def update_acceleration(self, delta_time, modulo: float = None):
        self.transform.acceleration = self.calculate_free_acceleration()
        if self.vehicle_before is not None:
            self.transform.acceleration += self.calculate_braking_interaction(self.vehicle_before, modulo)


class HDV(IDV):
    reaction_time: float
    variation_coefficient: float
    average_estimation_error: float
    distance_process: Wiener
    velocity_process: Wiener

    def __init__(self, *, position, velocity, acceleration, max_velocity, max_acceleration,
                 minimum_distance, headway_time, comfortable_deceleration,
                 reaction_time, variation_coefficient, average_estimation_error, correlation_times: float):
        self.reaction_time = reaction_time
        self.variation_coefficient = variation_coefficient
        self.average_estimation_error = average_estimation_error
        self.distance_process = Wiener(correlation_times)
        self.velocity_process = Wiener(correlation_times)
        super(HDV, self).__init__(position=position, velocity=velocity, acceleration=acceleration,
                                  max_velocity=max_velocity, max_acceleration=max_acceleration,
                                  minimum_distance=minimum_distance, headway_time=headway_time,
                                  comfortable_deceleration=comfortable_deceleration)

    def estimate_distance(self, other: Vehicle, modulo: float, time: float):
        estimated_distance = self.history[time].distance(other.history[time], modulo) *\
                             math.exp(self.variation_coefficient * self.distance_process.value)
        return estimated_distance

    def estimate_velocity_difference(self, other: Vehicle, modulo: float, time: float):
        estimated_velocity_diff = self.history[time].velocity_difference(other.history[time]) +\
               self.history[time].distance(other.history[time], modulo) *\
               self.average_estimation_error * self.velocity_process.value
        return estimated_velocity_diff

    def get_net_distance(self, other: Vehicle, modulo: float, time: float = -1):
        net_distance = self.estimate_distance(other, modulo, time) -\
               self.reaction_time * self.estimate_velocity_difference(other, modulo, time)
        return net_distance

    def get_velocity(self, time: float = -1):
        velocity = self.history[time].velocity -\
               self.reaction_time * self.history[time].acceleration
        return velocity

    def get_velocity_difference(self, other: Vehicle, modulo: float, time: float = -1):
        return self.history[time].velocity_difference(other.history[time])

    def calculate_free_acceleration(self, time: float = -1):
        return self.max_acceleration * (1 - (self.get_velocity(time) / self.max_velocity) ** 4)

    def calculate_desired_minimum_gap(self, other: Vehicle, modulo: float, time: float = -1):
        return self.minimum_distance + self.history[time].velocity * self.headway_time + \
            self.transform.velocity * self.get_velocity_difference(other, modulo) / \
            2 * math.sqrt(self.max_acceleration * self.comfortable_deceleration)

    def calculate_braking_interaction(self, other: Vehicle, modulo: float, time: float = -1):
        return -(self.max_acceleration *
                 (self.calculate_desired_minimum_gap(other, modulo, time) /
                  self.get_net_distance(other, modulo, time)) ** 2)

    def update_acceleration(self, delta_time, modulo: float = None):
        update_time = len(self.history) - 1 - self.reaction_time
        self.transform.acceleration = self.calculate_free_acceleration(update_time)
        if self.vehicle_before is not None:
            self.transform.acceleration += self.calculate_braking_interaction(self.vehicle_before, modulo, update_time)

    def simulate_step(self, delta_time, modulo: float = None):
        self.update_acceleration(delta_time, modulo)
        self.update_velocity(delta_time, modulo)
        self.update_position(delta_time, modulo)
        self.distance_process.update(delta_time)
        self.velocity_process.update(delta_time)


def vehicle_factory(name):
    if name == "Vehicle":
        def function(arglist: list):
            for i in range(len(arglist)):
                yield Vehicle(*arglist[i])
        return function
    if name == "IDV":
        def function(arglist: list):
            for i in range(len(arglist)):
                yield IDV(**arglist[i])
        return function
    if name == "HDV":
        def function(arglist: list):
            for i in range(len(arglist)):
                yield HDV(**arglist[i])
        return function


def get_vehicles(name, arglist):
    generator = vehicle_factory(name)(arglist)
    return [v for v in generator]