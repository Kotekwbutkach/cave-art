from . import VehicleData
from typing import List


class RoadData:
    road_length: float
    age: int
    vehicles_data: List[VehicleData]
    active_index: int
    looped: bool

    def __init__(self, road_length: float, looped: bool):
        self.road_length = road_length
        self.age = 0
        self.vehicles_data = list()
        self.active_index = 0
        self.looped = looped

    def __len__(self):
        return len(self.vehicles_data)

    def __getitem__(self, n: int):
        return self.vehicles_data[n]

    def add_vehicle_data(self, vehicle_data: VehicleData):
        self.vehicles_data.append(vehicle_data)

    def update(self):
        for vehicle_data in self.vehicles_data:
            vehicle_data.update()
        self.age += 1

    def set_inactive(self, number):
        self.active_index += number
