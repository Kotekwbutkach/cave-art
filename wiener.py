import math
import numpy


class Wiener:
    value: float
    correlation_time: float

    def __init__(self, correlation_time):
        self.value = 0
        self.correlation_time = correlation_time

    def update(self, delta_time):
        characteristic_time = delta_time / self.correlation_time
        normal_noise = numpy.random.normal(0, 1)
        self.value = math.exp(-characteristic_time) * self.value + math.sqrt(2 * characteristic_time) * normal_noise
