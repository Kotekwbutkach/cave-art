from road import CircleRoad
from graphics import VisibleCircleRoad


road = CircleRoad(1000.)
visibleRoad = VisibleCircleRoad(road, sps=40)

road.add_vehicles("IntelligentDriverController",
                  "HumanDriverView",
                  [{"position": 1000 - 40*x,
                    "velocity": 0,
                    "acceleration": 0,
                    "length": 5,
                    "awareness": 5,
                    "max_velocity": 20,
                    "max_acceleration": 1,
                    "minimum_distance": 2,
                    "headway_time": .5,
                    "comfortable_deceleration": 1.5,
                    "reaction_time": .1,
                    "variation_coefficient": 0.1,
                    "average_estimation_error_inverse": 0.01,
                    "correlation_times": 200}
                   for x in range(20)])
visibleRoad.simulate(0.1, 5000, autosave=2836)
road.data.show_plots(0, road.age)
