from data_structures import Transform, VehicleData, RoadData
from misc.wiener import Wiener
from typing import List, Tuple
import math


class ViewModule:
    awareness: int
    own_data: VehicleData
    other_data_list: List[VehicleData]

    def __init__(self, awareness: int, **kwargs):
        self.awareness = awareness

    def __repr__(self):
        return f"""ViewModule:
    awareness: {self.awareness}"""

    def get_view(self, road_data: RoadData):
        vehicle_id = self.own_data.vehicle_id
        if not road_data.looped:
            other_data_list = road_data.vehicles_data[road_data.active_index:vehicle_id]
        else:
            other_data_list = road_data.vehicles_data[vehicle_id+1:] + road_data.vehicles_data[:vehicle_id]
        self.other_data_list = other_data_list[-self.awareness:]

    def assemble(self, vehicle_data):
        self.own_data = vehicle_data
        return self

    def get_information(self, delta_time) -> Tuple[Transform, List[Transform]]:
        time_step = self.own_data.age() - 1
        return self.own_data.get_at(time_step),\
            [self.own_data.distance_at(vehicle_data, time_step) for vehicle_data in self.other_data_list]


class HumanDriverViewModule(ViewModule):
    reaction_time: float
    relative_distance_error: float
    inverse_average_estimation_error: float
    distance_process: Wiener
    velocity_process: Wiener

    def __init__(self, awareness: int,
                 reaction_time: float,
                 relative_distance_error: float,
                 inverse_average_estimation_error: float,
                 correlation_times: float,
                 **kwargs):
        self.reaction_time = reaction_time
        self.relative_distance_error = relative_distance_error
        self.inverse_average_estimation_error = inverse_average_estimation_error
        self.distance_process = Wiener(correlation_times)
        self.velocity_process = Wiener(correlation_times)
        super().__init__(awareness, **kwargs)

    def data_input(self, time_step):
        return self.own_data.get_at(time_step), \
            [self.own_data.distance_at(vehicle_data, time_step) for vehicle_data in self.other_data_list]

    def estimate_data(self, own_data, distances_list: List[Transform], time_step, delta_time):
        distance_estimations = list()
        for vehicle_distances in distances_list:
            distance = vehicle_distances.position
            velocity_difference = vehicle_distances.velocity
            estimated_position_difference = (distance *
                                             math.exp(self.relative_distance_error *
                                                      self.distance_process.get_value(time_step, delta_time)))
            estimated_velocity_difference = (velocity_difference + distance *
                                             self.inverse_average_estimation_error *
                                             self.velocity_process.get_value(time_step, delta_time))
            distance_estimation = Transform(estimated_position_difference,
                                            estimated_velocity_difference,
                                            vehicle_distances.acceleration)
            distance_estimations.append(distance_estimation)
        return own_data, distance_estimations

    def predict_data(self, own_data: Transform, distance_estimations: List[Transform]):
        position_prediction = (own_data.position + self.reaction_time * own_data.velocity +
                               ((self.reaction_time ** 2) / 2) * own_data.acceleration)
        velocity_prediction = own_data.velocity + self.reaction_time * own_data.acceleration
        own_prediction = Transform(position_prediction, velocity_prediction, own_data.acceleration)

        distance_predictions = list()
        for vehicle_estimations in distance_estimations:
            position_difference_prediction = (vehicle_estimations.position +
                                              self.reaction_time * vehicle_estimations.velocity)
            distance_prediction = Transform(position_difference_prediction,
                                            vehicle_estimations.velocity,
                                            vehicle_estimations.acceleration)
            distance_predictions.append(distance_prediction)
        return own_prediction, distance_predictions

    def get_information(self, delta_time):
        time_step = self.own_data.age() - 1 - (self.reaction_time / delta_time)
        own_data, distances_list = self.data_input(time_step)
        own_data, distances_list = self.estimate_data(own_data, distances_list, time_step, delta_time)
        own_data, distances_list = self.predict_data(own_data, distances_list)
        return own_data, distances_list


class ProportionalIntegralViewModule(ViewModule):
    m_steps: int

    def __init__(self, awareness: int,
                 m_steps: int,
                 **kwargs):
        super().__init__(awareness, **kwargs)
        self.m_steps = m_steps

    def get_information(self, delta_time) -> Tuple[Transform, List[Transform]]:
        time_step = self.own_data.age() - 1
        lead_data = self.other_data_list[-1][time_step]
        distance_data = self.own_data.distance_at(self.other_data_list[-1], time_step)
        own_time_data = self.own_data[time_step - self.m_steps + 1: time_step + 1]
        if not own_time_data:
            mean_data = Transform(0, 0, 0)
        else:
            mean_data = Transform(sum(data_step.position for data_step in own_time_data)/len(own_time_data),
                                  sum(data_step.velocity for data_step in own_time_data)/len(own_time_data),
                                  sum(data_step.acceleration for data_step in own_time_data)/len(own_time_data))
        return self.own_data.get_at(time_step), [lead_data, distance_data, mean_data]
