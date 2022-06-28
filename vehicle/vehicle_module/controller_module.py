from data_structures import Transform
from typing import Callable, List
import math


class ControllerModule:

    def __init__(self, **kwargs):
        pass

    def __repr__(self):
        return "ControllerModule"

    def acceleration_function(self) -> Callable:
        def acceleration(own_data: Transform,
                         other_data_list: List[Transform]
                         ) -> float:
            raise NotImplementedError
        return acceleration


class BaseControllerModule(ControllerModule):
    max_acceleration: float

    def __init__(self, max_acceleration, **kwargs):
        self.max_acceleration = max_acceleration
        super().__init__()

    def __repr__(self):
        return f"""BaseControllerModule:
    max_acceleration {self.max_acceleration}"""

    def acceleration_function(self) -> Callable:
        def acceleration(own_data: Transform,
                         other_data_list: List[Transform]
                         ) -> float:
            return self.max_acceleration
        return acceleration


class IntelligentDriverControllerModule(ControllerModule):
    max_acceleration: float
    max_velocity: float
    minimum_distance: float
    time_headway: float
    comfortable_deceleration: float

    def __init__(self,
                 max_acceleration: float,
                 max_velocity: float,
                 minimum_distance: float,
                 time_headway: float,
                 comfortable_deceleration: float,
                 **kwargs):
        self.max_acceleration = max_acceleration
        self.max_velocity = max_velocity
        self.minimum_distance = minimum_distance
        self.time_headway = time_headway
        self.comfortable_deceleration = comfortable_deceleration
        super().__init__()

    def __repr__(self):
        return f"""BaseControllerModule:
    max_acceleration: {self.max_acceleration}
    max_velocity: {self.max_velocity}
    minimum_distance: {self.minimum_distance}
    time_headway: {self.time_headway}
    comfortable_deceleration: {self.comfortable_deceleration}"""

    def acceleration_function(self) -> Callable:
        def acceleration(own_data: Transform,
                         distances_list: List[Transform]
                         ) -> float:
            coefficient = (1 - ((own_data.velocity / self.max_velocity) ** 4))
            for distance_data in distances_list:
                desired_minimum_gap = (self.minimum_distance +
                                       own_data.velocity * self.time_headway -
                                       (own_data.velocity * distance_data.velocity) /
                                       (2 * math.sqrt(self.max_acceleration * self.comfortable_deceleration)))
                coefficient -= ((desired_minimum_gap/distance_data.position) ** 2)
            return self.max_acceleration * coefficient
        return acceleration
