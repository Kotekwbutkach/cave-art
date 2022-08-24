from data_structures import Transform
from typing import Callable, List, Tuple, Dict
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
        return f"""IntelligentDriverControllerModule:
    max_acceleration: {self.max_acceleration}
    max_velocity: {self.max_velocity}
    minimum_distance: {self.minimum_distance}
    time_headway: {self.time_headway}
    comfortable_deceleration: {self.comfortable_deceleration}"""

    def acceleration_function(self) -> Callable:
        def acceleration(own_data: Transform,
                         distances_list: List[Transform]
                         ) -> float:
            velocity = max(own_data.velocity, 0)
            coefficient = 1 - (velocity / self.max_velocity) ** 4
            for distance_data in distances_list:
                desired_minimum_gap = (self.minimum_distance +
                                       velocity * self.time_headway -
                                       (velocity * distance_data.velocity) /
                                       (2 * math.sqrt(self.max_acceleration * self.comfortable_deceleration)))
                coefficient -= ((desired_minimum_gap/distance_data.position) ** 2)
            return self.max_acceleration * coefficient
        return acceleration


class FollowerStopperControllerModule(ControllerModule):
    max_velocity: float
    max_acceleration: float
    max_deceleration: float
    delta_x_0: Tuple[float, float, float]
    d: Tuple[float, float, float]

    def __init__(self, max_velocity: float, max_acceleration: float, max_deceleration: float,
                 delta_x_0: Tuple[float, float, float],
                 d: Tuple[float, float, float], **kwargs):
        super().__init__()
        self.max_velocity = max_velocity
        self.max_acceleration = max_acceleration
        self.max_deceleration = max_deceleration
        self.delta_x_0 = delta_x_0
        self.d = d

    def __repr__(self):
        return "FollowerStopperControllerModule"

    def acceleration_function(self) -> Callable:
        def h1(current_velocity, target_velocity):
            if target_velocity - current_velocity > 0:
                return self.max_acceleration
            return 0

        def h2(current_velocity, target_velocity):
            return -self.max_deceleration

        def acceleration(own_data: Transform,
                         distances_list: List[Transform]
                         ) -> float:
            delta_x = distances_list[-1].position
            delta_v = -distances_list[-1].velocity
            v = min(max(distances_list[-1].velocity + own_data.velocity, 0), self.max_velocity)

            delta_x_ = tuple(self.delta_x_0[k] + max(delta_v, 0) ** 2 / (2 * self.d[k]) for k in range(3))

            if delta_x > delta_x_[2]:
                v_cmd = self.max_velocity
            elif delta_x > delta_x_[1]:
                v_cmd = (self.max_velocity - v) * (delta_x - delta_x_[1]) / (delta_x_[2] - delta_x_[1])
            elif delta_x > delta_x_[0]:
                v_cmd = v * (delta_x - delta_x_[0]) / (delta_x_[1] - delta_x_[0])
            else:
                v_cmd = 0

            if v_cmd - own_data.velocity > -0.25:
                a = h1(own_data.velocity, v_cmd)
            else:
                a = h2(own_data.velocity, v_cmd)
            return a
        return acceleration


class ProportionalIntegralControllerModule(ControllerModule):
    v_catch: float
    gu: float
    gl: float
    gamma: float
    max_acceleration: float
    max_deceleration: float
    previous_v_cmd: float

    def __init__(self, v_catch: float,
                 gu: float,
                 gl: float,
                 gamma: float,
                 max_acceleration: float,
                 max_deceleration: float, **kwargs):
        super().__init__()
        self.v_catch = v_catch
        self.gu = gu
        self.gl = gl
        self.gamma = gamma
        self.max_acceleration = max_acceleration
        self.max_deceleration = max_deceleration
        self.previous_v_cmd = 0

    def __repr__(self):
        return "ProportionalIntegralControllerModule"

    def acceleration_function(self) -> Callable:
        def h1(current_velocity, target_velocity):
            if target_velocity - current_velocity > 0:
                return self.max_acceleration
            return 0

        def h2(current_velocity, target_velocity):
            return -self.max_deceleration

        def acceleration(own_data: Transform,
                         proportional_integral_view_list: List[Transform]
                         ) -> float:
            lead = proportional_integral_view_list[0]
            delta = proportional_integral_view_list[1]
            u = proportional_integral_view_list[2].velocity

            v_target = u + self.v_catch * min(max((delta.position - self.gl)/(self.gu - self.gl), 0), 1)
            delta_xs = max(2 * delta.velocity, 4)
            alpha = min(max(delta.position - delta_xs, 0), 1)
            beta = 1-(alpha/2)
            v_cmd = beta * (alpha * v_target + (1-alpha) * -lead.velocity) + (1-beta) * self.previous_v_cmd
            self.previous_v_cmd = v_cmd

            if v_cmd - own_data.velocity > -0.25:
                a = h1(own_data.velocity, v_cmd)
            else:
                a = h2(own_data.velocity, v_cmd)
            return a
        return acceleration


class VariableControlsControllerModule(ControllerModule):
    def __init__(self, *args: Tuple[ControllerModule, int]):
        super().__init__()
        self.time_step = 0
        self.controller_submodule_data = list(args)
        self.current_controller = self.controller_submodule_data[-1][0]

    def __repr__(self):
        string = f"VariableControlsControllerModule\n"
        for controller_submodule, _ in self.controller_submodule_data:
            string += str(controller_submodule) + "\n"
        return string

    def step(self):
        self.time_step += 1
        if len(self.controller_submodule_data) > 1 and self.time_step >= self.controller_submodule_data[-1][1]:
            self.controller_submodule_data.pop(-1)
            self.time_step = 0
            self.current_controller = self.controller_submodule_data[-1][0]

    def acceleration_function(self, *args, **kwargs) -> Callable:
        return self.current_controller.acceleration_function()
