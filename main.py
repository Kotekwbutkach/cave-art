from simulation import Simulation, default_simulation
from graphics import vehicle_plots, CircularRoadVisual, RoadVisual
from analysis import to_data_frame, csv_to_data_frame, velocity_std, throughput

number = 21
looped = True
road_length = 500
simulation_length = 10000

# Simulation 0

sim = default_simulation("sim0", number=number, road_length=road_length, simulation_length=simulation_length, show=True)

pos_df, vel_df, acc_df = to_data_frame(sim.road.data)

print(pos_df)
print(vel_df)
print(acc_df)
print(velocity_std(vel_df))
print(throughput(vel_df, road_length=road_length))

vis = CircularRoadVisual(sim.road, speed=3, screen_width=1000, screen_height=800)
vis.show()

# Simulation 1

sim = default_simulation("sim1", number=number, road_length=road_length, simulation_length=simulation_length, show=True,
                         arglist=[{"view_module": "ViewModule",
                                   "controller_module": "FollowerStopperDriverController",
                                   "max_acceleration": 1,
                                   "max_deceleration": 1.5,
                                   "delta_x_0": (4.5, 5.25, 6),
                                   "d": (1.5, 1, 0.5)}
                                  if n == 0 else None for n in range(number)])

pos_df, vel_df, acc_df = to_data_frame(sim.road.data)

print(pos_df)
print(vel_df)
print(acc_df)
print(velocity_std(vel_df))
print(throughput(vel_df, road_length=road_length))

vis = CircularRoadVisual(sim.road, speed=1, screen_width=1000, screen_height=800)
vis.show()

