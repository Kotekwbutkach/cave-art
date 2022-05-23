from typing import Callable, List
from data_structures import Transform
import math


class Controller:
    information: List[Transform]

    def __init__(self, **kwargs):
        self.information = list()

    def update_information(self, information: List[Transform]):
        self.information = information

    def acceleration_function(self) -> Callable:
        raise NotImplementedError


class TestController(Controller):
    max_acceleration: float

    def __init__(self, max_acceleration, **kwargs):
        self.max_acceleration = max_acceleration
        super(TestController, self).__init__()

    def acceleration_function(self) -> Callable:
        if self.information:
            def acceleration():
                return self.max_acceleration
        else:
            def acceleration():
                a = self.max_acceleration
                for transform_data in self.information[1:]:
                    a -= (transform_data.velocity - self.information[0].velocity)
                return a
        return acceleration


class IntelligentDriverController(Controller):
    max_velocity: float
    max_acceleration: float
    minimum_distance: float
    headway_time: float
    comfortable_deceleration: float

    def __init__(self, max_velocity, max_acceleration, minimum_distance, headway_time, comfortable_deceleration,
                 **kwargs):
        self.max_velocity = max_velocity
        self.max_acceleration = max_acceleration
        self.minimum_distance = minimum_distance
        self.headway_time = headway_time
        self.comfortable_deceleration = comfortable_deceleration

        super(IntelligentDriverController, self).__init__()

    def free_acceleration(self):
        return self.max_acceleration * (1 - (self.information[0].velocity / self.max_velocity) ** 4)

    def desired_minimum_gap(self, vehicle_id):
        return self.minimum_distance + self.information[0].velocity * self.headway_time + \
            self.information[0].velocity * self.information[vehicle_id].velocity / \
            (2 * math.sqrt(self.max_acceleration * self.comfortable_deceleration))

    def braking_interaction(self, vehicle_id):
        return -(self.max_acceleration *
                 (self.desired_minimum_gap(vehicle_id) /
                  self.information[vehicle_id].position) ** 2)

    def acceleration_function(self) -> Callable:
        def acceleration():
            a = self.free_acceleration()
            for vehicle_id in range(1, len(self.information)):
                a += self.braking_interaction(vehicle_id)
            return a
        return acceleration
