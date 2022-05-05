from typing import List
from vehicle import Transform, Vehicle
import matplotlib.pyplot as plt


class VehicleData:
    vehicle: Vehicle
    position: List[float]
    velocity: List[float]
    acceleration: List[float]

    def __init__(self, vehicle):
        self.vehicle = vehicle
        self.position = list()
        self.velocity = list()
        self.acceleration = list()

    def __getitem__(self, item):
        return self.position[item], self.velocity[item], self.acceleration[item]

    def __str__(self):
        return f"{str(self.position)}; {str(self.velocity)}; {str(self.acceleration)}"

    def update(self):
        self.position.append(self.vehicle.transform.position)
        self.velocity.append(self.vehicle.transform.velocity)
        self.acceleration.append(self.vehicle.current_acceleration)


class RoadData:
    vehicles_data: List[VehicleData]

    def __init__(self):
        self.vehicles_data = list()

    def __str__(self):
        string = ""
        if self.vehicles_data:
            for vehicle_data in self.vehicles_data:
                string += f"{vehicle_data}\n"
        return string

    def add_vehicle_data(self, vehicle_data: VehicleData):
        self.vehicles_data.append(vehicle_data)

    def update(self):
        for vehicle_data in self.vehicles_data:
            vehicle_data.update()

    def show_plot(self, start: int, end: int):
        for vehicle_data in self.vehicles_data:
            plt.plot(list(range(start, end)), vehicle_data.position[start:end], ",")
        plt.savefig("position.png", format="png")
        plt.show()
        for vehicle_data in self.vehicles_data:
            plt.plot(list(range(start, end)), vehicle_data.velocity[start:end], ",")
        plt.savefig("velocity.png", format="png")
        plt.show()
        for vehicle_data in self.vehicles_data:
            plt.plot(list(range(start, end)), vehicle_data.acceleration[start:end], ",")
        plt.savefig("acceleration.png", format="png")
        plt.show()