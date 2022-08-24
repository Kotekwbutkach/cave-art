from simulation import Simulation
from vehicle.vehicle_module import FollowerStopperControllerModule, IntelligentDriverControllerModule

# Experiment 1


vehicle_number = 21

print("Simulation without an autonomous vehicle:")
_, (std_dev_velocity, throughput) = Simulation.default_simulation("sim0",
                                                                  vehicle_number=vehicle_number,
                                                                  analyze=True)
print(std_dev_velocity)
print(throughput)

print("Simulation with a FS-driven autonomous vehicle:")
_, (std_dev_velocity, throughput) = Simulation.default_simulation("sim1",
                                                                  vehicle_number=vehicle_number,
                                                                  analyze=True,
                                                                  arglist=[
{"view_module": "View",
    "controller_module": "VariableControlsController",
    "controller_submodules": ((IntelligentDriverControllerModule(
                                                                 **{"max_acceleration": 1,
                                                                    "max_velocity": 36,
                                                                    "minimum_distance": 2,
                                                                    "time_headway": 0.7,
                                                                    "comfortable_deceleration": 1.5}),
                               1000),
                              (FollowerStopperControllerModule(
                                                                 **{"delta_x_0": (4.5, 5.25, 6),
                                                                    "d": (1.5, 1, 0.5),
                                                                    "max_velocity": 36,
                                                                    "max_acceleration": 1,
                                                                    "max_deceleration": 1.5}),
                               5000)),
    "delta_x_0": (4.5, 5.25, 6),
    "d": (1.5, 1, 0.5),
    "max_acceleration": 1,
    "max_deceleration": 1.5}
                                                                   if n == 0 else None for n in range(vehicle_number)])
print(std_dev_velocity)
print(throughput)
#
# print("Simulation with a PI-driven autonomous vehicle:")
# _, (std_dev_velocity, throughput) = Simulation.default_simulation("sim2", vehicle_number=vehicle_number,
#                                                                   analyze=True,
#                                                                   arglist=[{"view_module": "ProportionalIntegralView",
#                                                                             "controller_module": "ProportionalIntegralController",
#                                                                             "m_steps": 380,
#                                                                             "max_acceleration": 1,
#                                                                             "max_deceleration": 1.5,
#                                                                             "v_catch": 1,
#                                                                             "gu": 30,
#                                                                             "gl": 7,
#                                                                             "gamma": 2}
#                                                                            if n == 0 else None for n in
#                                                                            range(vehicle_number)])
# print(std_dev_velocity)
# print(throughput)
