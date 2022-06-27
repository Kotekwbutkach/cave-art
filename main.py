from simulation.simulation import Simulation
from graphics.visual import RoadVisual, CircularRoadVisual
from graphics.plot import vehicle_plots
from misc.debug import debug_function

number = 10
vehicle_parameters = [{"controller_module": "IntelligentDriverController",
                       "view_module": "View",
                       "position": 1000 - (1000*x)/number,
                       "velocity": 0,
                       "acceleration": 0,
                       "vehicle_length": 5,
                       "awareness": 5,
                       "max_acceleration": 1,
                       "max_velocity": 34,
                       "minimum_distance": 2,
                       "time_headway": 1.1,
                       "comfortable_deceleration": 1.5,
                       "reaction_time": 0.5,
                       "variation_coefficient": 0.05,
                       "average_estimation_error_inverse": 0.01,
                       "correlation_times": 20}
                      for x in range(number)]

sim = Simulation("sim1", circular=True, length=2000)
sim.road.add_vehicles(vehicle_parameters)

sim.simulate(0.1, 4000)

print([sim.road.data.vehicles_data[i][0].position for i in range(len(sim.road.data.vehicles_data))])
vis = CircularRoadVisual(sim.road, speed=4, screen_width=1000, screen_height=800)
vis.show()
vehicle_plots(sim)

# sim = Simulation("sim2", circular=True, length=260)
# sim.road.add_vehicles("IntelligentDriverController",
#                       "IntelligentDriverView",
#                       simulation_parameters)
#
# sim.simulate(0.1, 4000)
# vis = RoadVisual(sim.road, speed=1, screen_width=1000, screen_height=800)
# vis.show()
# vehicle_plots(sim)
