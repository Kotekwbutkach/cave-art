import math
import numpy as np


class Wiener:
    correlation_time: float
    value: float

    def __init__(self, correlation_time):
        self.value = 0
        self.correlation_time = correlation_time

    def get_value(self, time_step, delta_time):
        if time_step > 0:
            characteristic_time = delta_time / self.correlation_time
            normal_noise = np.random.normal(0, 1)
            self.value = math.exp(-characteristic_time) * self.value + math.sqrt(2 * characteristic_time) * normal_noise
        return self.value

