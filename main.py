from simulation import Simulation, default_simulation
from graphics import vehicle_plots, CircularRoadVisual, RoadVisual
from misc.debug import debug_function

number = 15
road_length = 260

# Simulation 0

sim = default_simulation("sim0", number=number, arglist=[{"view_module": "View"}
                                                         for _ in range(number)])

vis = CircularRoadVisual(sim.road, speed=2, screen_width=1000, screen_height=800)
vis.show()

# Simulation 1

sim = default_simulation("sim1", number=number, arglist=[{"relative_distance_error": 0.00,
                                                                 "inverse_average_estimation_error": 0.00}
                                                                for _ in range(number)])


vis = CircularRoadVisual(sim.road, speed=2, screen_width=1000, screen_height=800)
vis.show()

# Simulation 2

sim = default_simulation("sim2", number=number, arglist=[{"reaction_time": 0.00}
                                                         for _ in range(number)])

vis = CircularRoadVisual(sim.road, speed=2, screen_width=1000, screen_height=800)
vis.show()

# Simulation 3

sim = default_simulation("sim3", number=number)


vis = CircularRoadVisual(sim.road, speed=2, screen_width=1000, screen_height=800)
vis.show()
