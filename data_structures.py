import math
from typing import List
from transform import Transform
import matplotlib.pyplot as plt


class TransformData:
    transform: Transform
    position: List[float]
    velocity: List[float]
    acceleration: List[float]

    def __init__(self, transform):
        self.transform = transform
        self.position = [transform.position]
        self.velocity = [transform.velocity]
        self.acceleration = [transform.acceleration]

    def __str__(self):
        return f"{str(self.position)}; {str(self.velocity)}; {str(self.acceleration)}"

    def __len__(self):
        if len(self.position) == len(self.velocity) and len(self.position) == len(self.acceleration):
            return len(self.position)
        raise ValueError()

    def __getitem__(self, item):
        if item > len(self):
            return self[-1]
        if item < 0:
            return self[0]
        if type(item) == int:
            return Transform(self.position[item], self.velocity[item], self.acceleration[item])
        if type(item) == float:
            beta = 1 - item % 1
            return self[math.floor(item)] * beta + self[math.ceil(item)] * (1-beta)

    def update(self):
        self.position.append(self.transform.position)
        self.velocity.append(self.transform.velocity)
        self.acceleration.append(self.transform.acceleration)


class RoadData:
    vehicles_data: List[TransformData]

    def __init__(self):
        self.vehicles_data = list()

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
