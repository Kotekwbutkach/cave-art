from typing import Dict, List
from vehicle import Vehicle, produce_vehicles
from data_structures import RoadData


class Road:
    length: float
    age: int
    vehicles: List[Vehicle]
    data: RoadData

    def __init__(self, length: float, vehicles: List[Vehicle] = None, data: RoadData = None):
        self.length = length
        self.age = 0

        if vehicles is None:
            vehicles = list()
        self.vehicles = vehicles
        self.update_views()

        if data is None:
            data = RoadData()
        self.data = data

    def update_views(self):
        for i, v in enumerate(self.vehicles):
            if v.view.awareness is None:
                v.view.input_data = [v.history for v in self.vehicles[:i]]
            else:
                v.view.input_data = [v.history for v in self.vehicles[max(0, i-v.view.awareness):i]]

    def simulate_step(self, time_delta: float):
        to_remove = 0
        for vehicle in self.vehicles:
            vehicle.simulate_step(time_delta)
            if vehicle.physics.transform.position > self.length:
                to_remove += 1
        if to_remove > 0:
            self.remove_vehicles(to_remove)
        self.age += 1

    def simulate(self, time_delta: float, time_steps: int):
        for t in range(time_steps):
            self.simulate_step(time_delta)

    def add_vehicle(self, vehicle: Vehicle):
        self.vehicles.append(vehicle)
        self.data.add_vehicle(vehicle)
        self.update_views()

    def add_vehicles(self, controller_name: str, view_name, arglist: List[Dict]):
        generator = produce_vehicles(controller_name, view_name, arglist)
        for v in generator:
            self.add_vehicle(v)

    def remove_vehicles(self, n: int):
        self.vehicles = self.vehicles[n:]
        self.update_views()


class CircleRoad(Road):
    def simulate_step(self, time_delta: float):
        for vehicle in self.vehicles:
            vehicle.simulate_step(time_delta)
            if vehicle.physics.transform.position > self.length:
                vehicle.physics.transform.position -= self.length
        self.age += 1

    def add_vehicle(self, vehicle: Vehicle):
        vehicle.view.modulo = self.length
        self.vehicles.append(vehicle)
        self.data.add_vehicle(vehicle)
        self.update_views()

    def update_views(self):
        for i, v in enumerate(self.vehicles):
            if v.view.awareness is None:
                v.view.input_data = [v.history for v in self.vehicles[i+1:] + self.vehicles[:i]]
            else:
                input_data = self.vehicles[i+1:] + self.vehicles[:i]
                n = len(input_data)
                v.view.input_data = [v.history for v in input_data[n - 1 - v.view.awareness:]]