from road import CircleRoad
from graphics import VisibleCircleRoad

road = CircleRoad(260., debug=True)
visibleRoad = VisibleCircleRoad(road, sps=10, screen_width=1000, screen_height=800)


road.add_vehicles("IntelligentDriverController",
                  "HumanDriverView",
                  [{"position": 260 - (260*x)/21,
                    "velocity": 0,
                    "acceleration": 0,
                    "length": 5,
                    "awareness": 5,
                    "max_velocity": 25,
                    "max_acceleration": 1.5,
                    "minimum_distance": 2,
                    "headway_time": .5,
                    "comfortable_deceleration": 1.5,
                    "reaction_time": .8,
                    "variation_coefficient": 0.05,
                    "average_estimation_error_inverse": 0.01,
                    "correlation_times": 20}
                   for x in range(21)])
visibleRoad.simulate(0.1, 5000, autosave=500)
road.data.show_plots(0, road.age)
