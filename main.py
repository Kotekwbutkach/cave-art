from simulation import default_simulation

# Experiment 1

vehicle_number = 21
looped = True
road_length = 500
simulation_length = 100
repeats = 50

print("Simulation without an autonomous vehicle:")
std_dev_velocity, throughput = 0, 0
for i in range(repeats):
    _, (std, thr) = default_simulation(f"sim0_{i}", vehicle_number=vehicle_number, road_length=road_length,
                                       simulation_length=simulation_length, show=False, analyze=True)
    std_dev_velocity += std
    throughput += thr
print(std_dev_velocity/repeats)
print(throughput/repeats)

print("Simulation with a FS-driven autonomous vehicle:")
std_dev_velocity, throughput = 0, 0
for i in range(repeats):
    _, (std, thr) = default_simulation(f"sim1_{i}", vehicle_number=vehicle_number, road_length=road_length,
                                       simulation_length=simulation_length, show=False, analyze=True,
                                       arglist=[{"view_module": "View",
                                                 "controller_module": "FollowerStopperController",
                                                 "delta_x_0": (4.5, 5.25, 6),
                                                 "d": (1.5, 1, 0.5),
                                                 "max_acceleration": 1,
                                                 "max_deceleration": 1.5}
                                                if n == 0 else None for n in range(vehicle_number)])
    std_dev_velocity += std
    throughput += thr
print(std_dev_velocity/repeats)
print(throughput/repeats)

print("Simulation with a PI-driven autonomous vehicle:")
std_dev_velocity, throughput = 0, 0
for i in range(repeats):
    _, (std, thr) = default_simulation(f"sim2_{i}", vehicle_number=vehicle_number, road_length=road_length,
                                       simulation_length=simulation_length, show=False, analyze=True,
                                       arglist=[{"view_module": "ProportionalIntegralView",
                                                 "controller_module": "ProportionalIntegralController",
                                                 "m_steps": 380,
                                                 "max_acceleration": 1,
                                                 "max_deceleration": 1.5,
                                                 "v_catch": 1,
                                                 "gu": 30,
                                                 "gl": 7,
                                                 "gamma": 2}
                                                if n == 0 else None for n in range(vehicle_number)])
    std_dev_velocity += std
    throughput += thr
print(std_dev_velocity/repeats)
print(throughput/repeats)
