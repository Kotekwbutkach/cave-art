from typing import List
from data_structures import Transform, TransformData
from wiener import Wiener
import math


class View:
    own_data: TransformData
    input_data: List[TransformData]
    modulo: int
    awareness: int

    def __init__(self, own_data: TransformData = None, input_data: List[TransformData] = None,
                 awareness: int = None, modulo: int = None,
                 **kwargs):
        self.own_data = own_data

        if input_data is None:
            self.input_data = list()
        else:
            self.input_data = input_data

        self.awareness = awareness
        self.modulo = modulo

    def add_vehicle(self, transform_data: TransformData, position: int):
        self.input_data = self.input_data[:position] + [transform_data] + self.input_data[position:]
        if self.awareness is not None and position < self.awareness:
            self.input_data = self.input_data[:self.awareness]

    # data about other vehicles is relative to original transform
    def get_information(self, delta_time) -> List[Transform]:
        data = [self.own_data.get_at(-1)]
        for transform_data in self.input_data:
            new_entry = transform_data.get_at(-1) - self.own_data.get_at(-1)
            new_entry.position -= new_entry.length
            if self.modulo is not None:
                new_entry.position = new_entry.position % self.modulo
            data = data + [new_entry]
            new_entry.velocity = max(new_entry.velocity, 0)
        return data


class IntelligentDriverView(View):
    reaction_time: float

    def __init__(self, own_data: TransformData = None, input_data: List[TransformData] = None,
                 awareness: int = 1, reaction_time: float = 0,
                 **kwargs):
        self.reaction_time = reaction_time
        super(IntelligentDriverView, self).__init__(own_data, input_data, awareness)

        self.input_data = self.input_data[:awareness]

    def measurement_time(self, delta_time):
        time = len(self.own_data) - 1 - (self.reaction_time / delta_time)
        return time

    def predict_distance(self, transform_data, delta_time):
        time = self.measurement_time(delta_time)
        distance = (transform_data.get_at(time) - self.own_data.get_at(time)).position - transform_data.length -\
            self.reaction_time * (transform_data.get_at(time) - self.own_data.get_at(time)).velocity
        return distance

    def predict_velocity(self, delta_time):
        time = self.measurement_time(delta_time)
        velocity = self.own_data.get_at(time).velocity + self.reaction_time * self.own_data.get_at(time).acceleration
        return velocity

    def predict_velocity_difference(self, transform_data, delta_time):
        time = self.measurement_time(delta_time)
        return (transform_data.get_at(time) - self.own_data.get_at(time)).velocity

    def get_information(self, delta_time) -> List[TransformData]:
        time = self.measurement_time(delta_time)
        own_data = self.own_data.get_at(time)
        own_data.velocity = self.predict_velocity(delta_time)
        data = [own_data]
        for transform_data in self.input_data:
            new_entry = transform_data.get_at(time) - self.own_data.get_at(time)
            new_entry.position = self.predict_distance(transform_data, delta_time) - new_entry.length
            new_entry.velocity = self.predict_velocity_difference(transform_data, delta_time)
            if self.modulo is not None:
                new_entry.position = new_entry.position % self.modulo
            data = data + [new_entry]
        return data


class HumanDriverView(IntelligentDriverView):
    variation_coefficient: float
    average_estimation_error_inverse: float
    distance_process: Wiener
    velocity_process: Wiener

    def __init__(self, reaction_time: float = 0, awareness: int = 1,
                 own_data: TransformData = None, input_data: List[TransformData] = None,
                 variation_coefficient: float = 0, average_estimation_error_inverse: float = 0,
                 correlation_times: float = 20,
                 **kwargs):
        self.variation_coefficient = variation_coefficient
        self.average_estimation_error_inverse = average_estimation_error_inverse
        self.distance_process = Wiener(correlation_times)
        self.velocity_process = Wiener(correlation_times)
        super(HumanDriverView, self).__init__(own_data, input_data, awareness, reaction_time)

        self.input_data = self.input_data[:awareness]

    def measurement_time(self, delta_time):
        time = len(self.own_data) - 1 - (self.reaction_time / delta_time)
        return time

    def estimate_distance(self, transform_data, time):
        distance = (transform_data[time] - self.own_data.get_at(time)).position - transform_data.length
        return distance * math.exp(self.variation_coefficient * self.distance_process.value)

    def estimate_velocity_difference(self, transform_data, time):
        distance = (transform_data[time] - self.own_data.get_at(time)).position
        velocity_difference = (transform_data[time] - self.own_data.get_at(time)).velocity
        return velocity_difference + distance * self.average_estimation_error_inverse * self.velocity_process.value

    def predict_distance(self, transform_data, delta_time):
        time = self.measurement_time(delta_time)
        distance = self.estimate_distance(transform_data, time) -\
            self.reaction_time * self.estimate_velocity_difference(transform_data, time)
        return distance

    def predict_velocity(self, delta_time):
        time = self.measurement_time(delta_time)
        velocity = self.own_data.get_at(time).velocity + self.reaction_time * self.own_data.get_at(time).acceleration
        return velocity

    def predict_velocity_difference(self, transform_data, delta_time):
        time = self.measurement_time(delta_time)
        return self.estimate_velocity_difference(transform_data, time)
