from simulation import Simulation, default_simulation
from graphics import vehicle_plots, CircularRoadVisual, RoadVisual
from analysis import to_data_frame, csv_to_data_frame, velocity_std, throughput

number = 21
looped = True
road_length = 500

# Simulation 3

# sim = default_simulation("sim3", number=number, road_length=road_length, show=True)

# pos_df, vel_df, acc_df = to_data_frame(sim.road.data)

pos_df, vel_df, acc_df = csv_to_data_frame("output/sim3")

print(velocity_std(vel_df))
print(throughput(vel_df, road_length=road_length))

# vis = CircularRoadVisual(sim.road, speed=1, screen_width=1000, screen_height=800)
# vis.show()
