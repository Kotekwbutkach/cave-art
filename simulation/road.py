from vehicle.vehicle import Vehicle, produce_vehicles
from data_structures.road_data import RoadData
from typing import Dict, List


class Road:
    vehicles: List[Vehicle]
    data: RoadData

    def __init__(self, length: float, vehicles: List[Vehicle] = None):

        if vehicles is None:
            vehicles = list()
        self.vehicles = vehicles
        self.update_views()
        self.data = RoadData(length, looped=False)

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
            if vehicle.physics.transform.position > self.data.length:
                vehicle.physics.transform.set_values(self.data.length, 0, 0, vehicle.physics.transform.length)
                to_remove += 1
        if to_remove > 0:
            self.remove_vehicles(to_remove)
        self.data.update()

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


class CircularRoad(Road):
    def __init__(self, length: float, vehicles: List[Vehicle] = None):
        super().__init__(length, vehicles)
        self.data.looped = True

    def simulate_step(self, time_delta: float):
        for vehicle in self.vehicles:
            vehicle.simulate_step(time_delta)
            if vehicle.physics.transform.position > self.data.length or vehicle.physics.transform.position < 0:
                vehicle.physics.transform.position = vehicle.physics.transform.position % self.data.length
        self.data.update()

    def add_vehicle(self, vehicle: Vehicle):
        vehicle.view.modulo = self.data.length
        self.vehicles.append(vehicle)
        self.data.add_vehicle(vehicle)
        self.update_views()

    def update_views(self):
        for i, v in enumerate(self.vehicles):
            if v.view.awareness is None:
                v.view.input_data = [v.history for v in self.vehicles[i + 1:] + self.vehicles[:i]]
            else:
                input_data = self.vehicles[i+1:] + self.vehicles[:i]
                n = len(input_data)
                v.view.input_data = [v.history for v in input_data[max(n - 1 - v.view.awareness, 0):]]
