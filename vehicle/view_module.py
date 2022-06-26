from typing import List
from data_structures.transform import Transform
from data_structures.vehicle_data import VehicleData
from misc.wiener import Wiener
import math


class View:
    own_data: VehicleData
    input_data: List[VehicleData]
    modulo: int
    awareness: int

    def __init__(self, own_data: VehicleData = None, input_data: List[VehicleData] = None,
                 awareness: int = None, modulo: int = None,
                 **kwargs):
        self.own_data = own_data

        if input_data is None:
            self.input_data = list()
        else:
            self.input_data = input_data

        self.awareness = awareness
        self.modulo = modulo

    def add_vehicle(self, vehicle_data: VehicleData, position: int):
        self.input_data = self.input_data[:position] + [vehicle_data] + self.input_data[position:]
        if self.awareness is not None and position < self.awareness:
            self.input_data = self.input_data[:self.awareness]

    # data about other vehicles is relative to original transform
    def get_information(self, delta_time) -> List[Transform]:
        data = [self.own_data.get_at(-1)]
        for vehicle_data in self.input_data:
            new_entry = vehicle_data.get_at(-1) - self.own_data.get_at(-1)
            new_entry.position -= new_entry.length
            if self.modulo is not None:
                new_entry.position = new_entry.position % self.modulo
            data.append(new_entry)
            new_entry.velocity = max(new_entry.velocity, 0)
        return data


class IntelligentDriverView(View):
    reaction_time: float

    def __init__(self, own_data: VehicleData = None, input_data: List[VehicleData] = None,
                 awareness: int = 1, reaction_time: float = 0,
                 **kwargs):
        self.reaction_time = reaction_time
        super().__init__(own_data, input_data, awareness)

        self.input_data = self.input_data[:awareness]

    def measurement_time(self, delta_time):
        time = len(self.own_data) - 1 - (self.reaction_time / delta_time)
        return time

    def predict_distance(self, vehicle_data, delta_time):
        time = self.measurement_time(delta_time)

        delayed_distance = ((vehicle_data.get_at(time, self.modulo) -
                             self.own_data.get_at(time, self.modulo)).position
                            - vehicle_data.length)
        if self.modulo is not None:
            delayed_distance = delayed_distance % self.modulo

        predicted_distance = delayed_distance + self.reaction_time * (vehicle_data.get_at(time, self.modulo) -
                                                                      self.own_data.get_at(time, self.modulo)).velocity\
            + self.reaction_time ** 2 / 2 * self.own_data.get_at(time, self.modulo).acceleration
        return predicted_distance

    def predict_velocity(self, delta_time):
        time = self.measurement_time(delta_time)
        velocity = self.own_data.get_at(time, self.modulo).velocity + self.reaction_time\
            * self.own_data.get_at(time, self.modulo).acceleration
        return velocity

    def predict_velocity_difference(self, vehicle_data, delta_time):
        time = self.measurement_time(delta_time)
        return (vehicle_data.get_at(time, self.modulo) - self.own_data.get_at(time, self.modulo)).velocity

    def get_information(self, delta_time) -> List[VehicleData]:
        time = self.measurement_time(delta_time)
        own_data = self.own_data.get_at(time, self.modulo)
        own_data.velocity = self.predict_velocity(delta_time)
        data = [own_data]
        for vehicle_data in self.input_data:
            new_entry = vehicle_data.get_at(time, self.modulo) - self.own_data.get_at(time, self.modulo)
            new_entry.position = self.predict_distance(vehicle_data, delta_time)
            new_entry.velocity = self.predict_velocity_difference(vehicle_data, delta_time)
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
                 own_data: VehicleData = None, input_data: List[VehicleData] = None,
                 variation_coefficient: float = 0, average_estimation_error_inverse: float = 0,
                 correlation_times: float = 20,
                 **kwargs):
        self.variation_coefficient = variation_coefficient
        self.average_estimation_error_inverse = average_estimation_error_inverse
        self.distance_process = Wiener(correlation_times)
        self.velocity_process = Wiener(correlation_times)
        super().__init__(own_data, input_data, awareness, reaction_time)

        self.input_data = self.input_data[:awareness]

    def estimate_distance(self, vehicle_data, time):
        distance = (vehicle_data.get_at(time, self.modulo) - self.own_data.get_at(time, self.modulo)).position\
                   - vehicle_data.length
        return distance * math.exp(self.variation_coefficient * self.distance_process.value)

    def estimate_velocity_difference(self, vehicle_data, time):
        distance = (vehicle_data.get_at(time, self.modulo) - self.own_data.get_at(time, self.modulo)).position
        velocity_difference = (vehicle_data.get_at(time, self.modulo) - self.own_data.get_at(time, self.modulo))\
            .velocity
        return velocity_difference + distance * self.average_estimation_error_inverse * self.velocity_process.value

    def predict_distance(self, vehicle_data, delta_time):
        time = self.measurement_time(delta_time)
        distance = self.estimate_distance(vehicle_data, time) +\
            self.reaction_time * self.estimate_velocity_difference(vehicle_data, time)
        return distance

    def predict_velocity(self, delta_time):
        time = self.measurement_time(delta_time)
        velocity = self.own_data.get_at(time, self.modulo).velocity \
            + self.reaction_time * self.own_data.get_at(time, self.modulo).acceleration
        return velocity

    def predict_velocity_difference(self, vehicle_data, delta_time):
        time = self.measurement_time(delta_time)
        return self.estimate_velocity_difference(vehicle_data, time)
