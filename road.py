import copy
from typing import List
from vehicle import Vehicle
from data_structures import VehicleData, RoadData


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
        else:
            vehicles[0].vehicle_before = None
            for i in range(1, len(vehicles)):
                vehicles[i].vehicle_before = vehicles[i-1]
        self.vehicles = vehicles

        if data is None:
            data = RoadData()
        self.data = data

    def simulate_step(self, time_delta: float):
        self.vehicles[0].simulate_step(time_delta)
        to_remove = 0
        for i in range(1, len(self.vehicles)):
            self.vehicles[i].simulate_step(time_delta)
            if self.vehicles[i].transform.position > self.length:
                to_remove += 1
        self.data.update()
        if to_remove > 0:
            self.remove_vehicles(to_remove)
        self.age += 1

    def simulate(self, time_delta: float, time_steps: int):
        for t in range(time_steps):
            self.simulate_step(time_delta)

    def add_vehicle(self, vehicle: Vehicle):
        if self.vehicles:
            vehicle.vehicle_before = self.vehicles[-1]
        self.vehicles.append(vehicle)
        self.data.add_vehicle_data(VehicleData(vehicle))

    def add_vehicles(self, vehicle: Vehicle, num: int, starting_distance):
        for i in range(num):
            vehicle_copy = copy.deepcopy(vehicle)
            vehicle_copy.transform.position += starting_distance * (num-1-i)
            self.add_vehicle(vehicle_copy)

    def remove_vehicles(self, i: int):
        self.vehicles = self.vehicles[i:]
        self.vehicles[0].vehicle_before = None


class CircleRoad(Road):

    def simulate_step(self, time_delta: float):
        self.vehicles[0].simulate_step(time_delta, self.length)
        for i in range(1, len(self.vehicles)):
            self.vehicles[i].simulate_step(time_delta, self.length)
        self.data.update()
        self.age += 1

    def add_vehicle(self, vehicle: Vehicle):
        if self.vehicles:
            vehicle.vehicle_before = self.vehicles[-1]
            self.vehicles[0].vehicle_before = vehicle
        else:
            vehicle.vehicle_before = vehicle
        self.vehicles.append(vehicle)
        self.data.add_vehicle_data(VehicleData(vehicle))
