from simulation.simulation import Simulation
from graphics.visual import RoadVisual, CircularRoadVisual
from graphics.plot import vehicle_plots
from misc.debug import debug_function

number = 15
road_length = 260

# Simulation 0

vehicle_parameters = [{"controller_module": "IntelligentDriverController",
                       "view_module": "View",
                       "position": road_length/2 - (road_length*x)/(2 * number),
                       "velocity": 0,
                       "acceleration": 0,
                       "vehicle_length": 5,
                       "awareness": 5,
                       "max_acceleration": 1,
                       "max_velocity": 25,
                       "minimum_distance": 2,
                       "time_headway": 0.5,
                       "comfortable_deceleration": 1.5,
                       "reaction_time": 1,
                       "relative_distance_error": 0.00,
                       "inverse_average_estimation_error": 0.00,
                       "correlation_times": 20}
                      for x in range(number)]

sim = Simulation("sim0", circular=True, length=road_length)
sim.road.add_vehicles(vehicle_parameters)

sim.simulate(0.1, 10000)
vehicle_plots(sim, end=sim.road.data.age-45)
# vis = CircularRoadVisual(sim.road, speed=2, screen_width=1000, screen_height=800)
# vis.show()

# Simulation 1

vehicle_parameters = [{"controller_module": "IntelligentDriverController",
                       "view_module": "HumanDriverView",
                       "position": road_length/2 - (road_length*x)/(2 * number),
                       "velocity": 0,
                       "acceleration": 0,
                       "vehicle_length": 5,
                       "awareness": 5,
                       "max_acceleration": 1,
                       "max_velocity": 25,
                       "minimum_distance": 2,
                       "time_headway": 0.5,
                       "comfortable_deceleration": 1.5,
                       "reaction_time": 0.5,
                       "relative_distance_error": 0.00,
                       "inverse_average_estimation_error": 0.00,
                       "correlation_times": 20}
                      for x in range(number)]

sim = Simulation("sim1", circular=True, length=road_length)
sim.road.add_vehicles(vehicle_parameters)

sim.simulate(0.1, 8000)
vehicle_plots(sim, end=sim.road.data.age-45)
vehicle_plots(sim, end=1000)
vehicle_plots(sim, start=1000, end=4500)
vehicle_plots(sim, start=4500, end=8000)
# vis = CircularRoadVisual(sim.road, speed=2, screen_width=1000, screen_height=800)
# vis.show()

# Simulation 2

# vehicle_parameters = [{"controller_module": "IntelligentDriverController",
#                        "view_module": "HumanDriverView",
#                        "position": road_length - (road_length*x)/number,
#                        "velocity": 0,
#                        "acceleration": 0,
#                        "vehicle_length": 5,
#                        "awareness": 5,
#                        "max_acceleration": 1,
#                        "max_velocity": 25,
#                        "minimum_distance": 2,
#                        "time_headway": 0.5,
#                        "comfortable_deceleration": 1.5,
#                        "reaction_time": 1,
#                        "relative_distance_error": 0.05,
#                        "inverse_average_estimation_error": 0.01,
#                        "correlation_times": 20}
#                       for x in range(number)]
#
# sim = Simulation("sim2", circular=True, length=road_length)
# sim.road.add_vehicles(vehicle_parameters)
#
# sim.simulate(0.1, 1200)
# vis = CircularRoadVisual(sim.road, speed=5, screen_width=1000, screen_height=800)
# vis.show()
# vehicle_plots(sim, end=sim.road.data.age-45)
