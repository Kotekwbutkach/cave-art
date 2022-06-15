from road import CircleRoad
from graphics import VisibleCircleRoad
import debug

length = 260
number = 10


road = CircleRoad(length)
visibleRoad = VisibleCircleRoad(road, sps=60, screen_width=1000, screen_height=800,
                                debug_function=debug.debug_function)


road.add_vehicles("IntelligentDriverController",
                  "View",
                  #"IntelligentDriverView",
                  [{"position": 260 - (260*x)/number,
                    "velocity": 0,
                    "acceleration": 0,
                    "length": 5,
                    "awareness": 5,
                    "max_velocity": 15,
                    "max_acceleration": 1.5,
                    "minimum_distance": 2,
                    "headway_time": .5,
                    "comfortable_deceleration": 1.5,
                    "reaction_time": .1,
                    "variation_coefficient": 0.05,
                    "average_estimation_error_inverse": 0.01,
                    "correlation_times": 20}
                   for x in range(number)])
visibleRoad.simulate(0.1, 8000, autosave=5000)
road.data.show_plots(0, road.age)
