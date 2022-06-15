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
        return Transform(scale * self.position, scale * self.velocity, scale * self.acceleration, self.length)

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

    def get_at(self, i, modulo=None):
        if i > len(self) - 1 or i == -1:
            return self.get_at(len(self)-1)
        if i < 0:
            return self.get_at(0)
        if type(i) == int:
            return Transform(self.position[i], self.velocity[i], self.acceleration[i], self.length)
        if type(i) == float:
            beta = 1 - i % 1
            if modulo is None:
                return self.get_at(math.floor(i)) * beta + self.get_at(math.ceil(i)) * (1 - beta)

            value_before = self.get_at(math.floor(i))
            value_after = self.get_at(math.ceil(i))

            if (value_before.position > (modulo * 2/3)) and (value_after.position < (modulo * 1/3)):  # passed the modulo wrap
                value_after.position += modulo
            elif (value_before.position < (modulo * 1/3)) and (value_after.position > (modulo * 2/3)):  # reverse passed the modulo wrap
                value_before.position += modulo

            value = (value_before * beta + value_after * (1 - beta))
            value.position = value.position % modulo
            return value

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
