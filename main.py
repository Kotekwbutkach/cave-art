from simulation.simulation import Simulation
from graphics.visual import RoadVisual, CircularRoadVisual
from graphics.plot import vehicle_plots


number = 10
simulation_parameters = [{"position": 1000 - (1000*x)/number,
                          "velocity": 0,
                          "acceleration": 0,
                          "length": 5,
                          "awareness": 5,
                          "max_velocity": 34,
                          "max_acceleration": 1,
                          "minimum_distance": 2,
                          "headway_time": 1.1,
                          "comfortable_deceleration": 1.5,
                          "reaction_time": 0.5,
                          "variation_coefficient": 0.05,
                          "average_estimation_error_inverse": 0.01,
                          "correlation_times": 20}
                         for x in range(number)]


sim = Simulation("sim1", circular=True, length=2000)
sim.road.add_vehicles("IntelligentDriverController",
                      "View",
                      simulation_parameters)

sim.simulate(0.1, 4000)
vis = CircularRoadVisual(sim.road, speed=1, screen_width=1000, screen_height=800)
vis.show()
vehicle_plots(sim, end=1250)

# sim = Simulation("sim2", circular=True, length=260)
# sim.road.add_vehicles("IntelligentDriverController",
#                       "IntelligentDriverView",
#                       simulation_parameters)
#
# sim.simulate(0.1, 4000)
# vis = RoadVisual(sim.road, speed=1, screen_width=1000, screen_height=800)
# vis.show()
# vehicle_plots(sim)
