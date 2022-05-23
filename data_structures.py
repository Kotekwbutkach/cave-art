import math
from typing import List
import matplotlib.pyplot as plt
import csv


class Transform:
    position: float
    velocity: float
    acceleration: float
    length: float

    def __init__(self, position, velocity, acceleration, length=0.):
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.length = length

    def __str__(self):
        return f"{str(self.position)}; {str(self.velocity)}; {str(self.acceleration)}"

    def __add__(self, other: "Transform"):
        return Transform(self.position + other.position,
                         self.velocity + other.velocity,
                         self.acceleration + other.acceleration,
                         self.length)

    def __sub__(self, other: "Transform"):
        return Transform(self.position - other.position,
                         self.velocity - other.velocity,
                         self.acceleration - other.acceleration,
                         self.length)

    def __mul__(self, scale: float):
        return Transform(scale * self.position, scale * self.velocity, scale * self.acceleration, scale * self.length)

    def distance(self, other, modulo: float = None):
        dist = other.position - other.length - self.position
        if modulo is not None:
            dist = dist % modulo
        return dist

    def velocity_difference(self, other):
        return self.velocity - other.velocity


class TransformData:
    transform: Transform
    position: List[float]
    velocity: List[float]
    acceleration: List[float]
    length: float

    def __init__(self, transform):
        self.transform = transform
        self.position = [transform.position]
        self.velocity = [transform.velocity]
        self.acceleration = [transform.acceleration]
        self.length = transform.length

    def __str__(self):
        return f"{str(self.position)}; {str(self.velocity)}; {str(self.acceleration)}; {str(self.length)}"

    def __len__(self):
        if len(self.position) == len(self.velocity) and len(self.position) == len(self.acceleration):
            return len(self.position)
        raise ValueError()

    def __getitem__(self, item):
        if item > len(self) - 1:
            return self[-1]
        if item < 0:
            return self[0]
        if type(item) == int:
            return Transform(self.position[item], self.velocity[item], self.acceleration[item], self.length)
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

    def show_plots(self, start: int, end: int):
        for vehicle_data in self.vehicles_data:
            plt.plot(list(range(start, end)), vehicle_data.position[start:end], ",")
        plt.savefig("graphs/position.png", format="png")
        plt.show()
        for vehicle_data in self.vehicles_data:
            plt.plot(list(range(start, end)), vehicle_data.velocity[start:end], ",")
        plt.savefig("graphs/velocity.png", format="png")
        plt.show()
        for vehicle_data in self.vehicles_data:
            plt.plot(list(range(start, end)), vehicle_data.acceleration[start:end], ",")
        plt.savefig("graphs/acceleration.png", format="png")
        plt.show()

    def save_to_csv(self):
        with open('output/position.csv', 'w', newline='') as csvfile:
            data_writer = csv.writer(csvfile, delimiter=';')
            for line in range(len(self.vehicles_data[0])):
                data_writer.writerow([self.vehicles_data[i].position[line] for i in range(len(self.vehicles_data))])
        with open('output/velocity.csv', 'w', newline='') as csvfile:
            data_writer = csv.writer(csvfile, delimiter=';')
            for line in range(len(self.vehicles_data[0])):
                data_writer.writerow([self.vehicles_data[i].velocity[line] for i in range(len(self.vehicles_data))])
        with open('output/acceleration.csv', 'w', newline='') as csvfile:
            data_writer = csv.writer(csvfile, delimiter=';')
            for line in range(len(self.vehicles_data[0])):
                data_writer.writerow([self.vehicles_data[i].acceleration[line] for i in range(len(self.vehicles_data))])
