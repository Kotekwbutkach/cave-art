from road import CircleRoad
from graphics import VisibleRoad, VisibleRoundRoad
from vehicle import TestVehicle, IDV


'''road = CircleRoad(10.)
# visibleRoad = VisibleRoad(road)
visibleRoad = VisibleRoundRoad(road)
print(road.data)
road.add_vehicle(TestVehicle(9, 0))
road.add_vehicle(TestVehicle(6, 0))
road.add_vehicle(TestVehicle(3, 0))
road.add_vehicle(TestVehicle(0, 0))
print(road.data)
visibleRoad.simulate(0.01, 10000)
print(road.data)
road.data.show_plot(0, road.age)'''

road = CircleRoad(10.)
visibleRoad = VisibleRoundRoad(road, sps=0.1)
road.add_vehicles(IDV(0, 0, 2, 1, 0.02, 0.5, 0.5), 3, 0.5)
visibleRoad.simulate(0.01, 10000)
print(road.data)
road.data.show_plot(0, road.age)