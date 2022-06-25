from .vehicle_data import VehicleData
from typing import List
import csv


class RoadData:
    length: float
    age: int
    vehicles_data: List[VehicleData]
    looped: bool

    def __init__(self, length, looped):
        self.length = length
        self.age = 0
        self.vehicles_data = list()
        self.looped = looped

    def __str__(self):
        string = ""
        if self.vehicles_data:
            for vehicle_data in self.vehicles_data:
                string += f"{vehicle_data}\n"
        return string

    def __len__(self):
        return len(self.vehicles_data)

    def __getitem__(self, item):
        return self.vehicles_data[item]

    def add_vehicle(self, vehicle):
        self.vehicles_data.append(vehicle.history)

    def update(self):
        for vehicle_data in self.vehicles_data:
            vehicle_data.update()
        self.age += 1

    def save_to_csv(self, simulation_name=""):
        with open(f'output/{simulation_name}_position.csv', 'w', newline='') as csvfile:
            data_writer = csv.writer(csvfile, delimiter=';')
            for line in range(self.age):
                data_writer.writerow([self.vehicles_data[i].position[line] for i in range(len(self.vehicles_data))])
        with open(f'output/{simulation_name}_velocity.csv', 'w', newline='') as csvfile:
            data_writer = csv.writer(csvfile, delimiter=';')
            for line in range(self.age):
                data_writer.writerow([self.vehicles_data[i].velocity[line] for i in range(len(self.vehicles_data))])
        with open(f'output/{simulation_name}_acceleration.csv', 'w', newline='') as csvfile:
            data_writer = csv.writer(csvfile, delimiter=';')
            for line in range(self.age):
                data_writer.writerow([self.vehicles_data[i].acceleration[line] for i in range(len(self.vehicles_data))])
