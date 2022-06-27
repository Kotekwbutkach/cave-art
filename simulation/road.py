from vehicle.vehicle import Vehicle
from data_structures.road_data import RoadData
from data_structures.transform import Transform
from typing import Dict, List


class Road:
    vehicles: List[Vehicle]
    data: RoadData

    def __init__(self, length: float):
        self.vehicles = list()
        self.data = RoadData(length, looped=False)

    def simulate_step(self, delta_time: float):
        to_remove = 0
        for vehicle in self.vehicles:
            vehicle.simulate_step(self.data, delta_time)
            if vehicle.physics.transform.position >= self.data.road_length:
                vehicle.physics.transform = Transform(self.data.road_length, 0, 0)
                to_remove += 1
        self.data.update()
        if to_remove > 0:
            self.remove_vehicles(to_remove)

    def add_vehicle(self, **kwargs):
        vehicle = Vehicle.from_kwargs(self.data, **kwargs)
        self.vehicles.append(vehicle)
        self.data.add_vehicle_data(vehicle.data)

    def add_vehicles(self, arglist: List[Dict]):
        for v in Vehicle.generate_vehicles(self.data, arglist):
            self.vehicles.append(v)
            self.data.add_vehicle_data(v.data)

    def remove_vehicles(self, n: int):
        self.vehicles = self.vehicles[n:]
        self.data.set_inactive(n)


class CircularRoad(Road):
    def __init__(self, length: float):
        super().__init__(length)
        self.data.looped = True

    def simulate_step(self, delta_time: float):
        for vehicle in self.vehicles:
            vehicle.simulate_step(self.data, delta_time)
            if vehicle.physics.transform.position > self.data.road_length or vehicle.physics.transform.position < 0:
                vehicle.physics.transform.position = vehicle.physics.transform.position % self.data.road_length
        self.data.update()
