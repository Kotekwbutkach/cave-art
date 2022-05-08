from road import CircleRoad
from graphics import VisibleCircleRoad
"""
road = CircleRoad(15.)
visibleRoad = VisibleCircleRoad(road, sps=20)

road.add_vehicles("IDV", [{"position": 2.5 - x/2,
                           "velocity": 0,
                           "acceleration": 0,
                           "max_velocity": 5,
                           "max_acceleration": 2,
                           "minimum_distance": .1,
                           "headway_time": .5,
                           "comfortable_deceleration": 0.5} for x in range(5)])
visibleRoad.simulate(0.01, 10000)
road.data.show_plot(0, road.age)
"""
road = CircleRoad(15.)
visibleRoad = VisibleCircleRoad(road, sps=40)

road.add_vehicles("HDV", [{"position": 2.5 - x/2,
                           "velocity": 0,
                           "acceleration": 0,
                           "max_velocity": 25,
                           "max_acceleration": 2,
                           "minimum_distance": .1,
                           "headway_time": .5,
                           "comfortable_deceleration": 0.5,
                           "reaction_time": 0.1,
                           "variation_coefficient": 0,
                           "average_estimation_error": 1,
                           "correlation_times": 1} for x in range(5)])
visibleRoad.simulate(0.001, 20000)
road.data.show_plot(0, road.age)
