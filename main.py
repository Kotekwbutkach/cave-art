from simulation.simulation import Simulation
from graphics.visuals import RoadVisual

number = 10

simulation = Simulation("sim1", length=260)
simulation.road.add_vehicles("IntelligentDriverController",
                             "View",
                             [{"position": 130 - (130*x)/number,
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

simulation.simulate(0.1, 1000)
visual = RoadVisual(simulation.road, speed=1, screen_width=1000, screen_height=800)
visual.show()
