from simulation import Simulation
from vehicle.vehicle_module import FollowerStopperControllerModule, IntelligentDriverControllerModule, \
    HumanDriverViewModule, ProportionalIntegralViewModule, ProportionalIntegralControllerModule

# Experiment 1


vehicle_number = 21


def simulation_0():
    print("Simulation without an autonomous vehicle:")

    _, (std_dev_velocity, throughput) = Simulation.default_simulation(
        "sim0",
        vehicle_number=vehicle_number,
        analyze=True)

    print(std_dev_velocity)
    print(throughput)


def simulation_1():
    print("Simulation with a FS-driven autonomous vehicle:")

    _, (std_dev_velocity, throughput) = Simulation.default_simulation(
        "sim1",
        vehicle_number=vehicle_number,
        analyze=True,
        arglist=[
            {
                "view_module": "HumanDriverView",
                "controller_module": "VariableControlsController",
                "controller_submodules": (
                    (IntelligentDriverControllerModule(
                        **{
                            "max_acceleration": 1,
                            "max_velocity": 36,
                            "minimum_distance": 2,
                            "time_headway": 0.7,
                            "comfortable_deceleration": 1.5}),
                        3000),
                    (FollowerStopperControllerModule(
                        **{
                            "delta_x_0": (4.5, 5.25, 6),
                            "d": (1.5, 1, 0.5),
                            "max_velocity": 6.5,
                            "max_acceleration": 1,
                            "max_deceleration": 1.5}),
                        3000)),
                "awareness": 5,
                "comfortable_deceleration": 1.5,
                "reaction_time": 0.5,
                "relative_distance_error": 0.05,
                "inverse_average_estimation_error": 0.01
            }
            if n == 0 else None for n in range(vehicle_number)])

    print(std_dev_velocity)
    print(throughput)


def simulation_2():
    print("Simulation with a PI-driven autonomous vehicle:")
    _, (std_dev_velocity, throughput) = Simulation.default_simulation(
        "sim2",
        vehicle_number=vehicle_number,
        analyze=True,
        simulation_length=6000,
        arglist=[
            {
                "view_module": "VariableViewsView",
                "view_submodules": (
                    (HumanDriverViewModule(
                        **{
                            "awareness": 5,
                            "reaction_time": 0.5,
                            "relative_distance_error": 0.1,
                            "inverse_average_estimation_error": 0.01,
                            "correlation_times": 200
                        }),
                        3000),
                    (ProportionalIntegralViewModule(
                        **{
                            "awareness": 5,
                            "m_steps": 380
                        }),
                        3000)),
                "controller_module": "VariableControlsController",
                "controller_submodules": (
                    (IntelligentDriverControllerModule(
                        **{
                            "max_acceleration": 1,
                            "max_velocity": 36,
                            "minimum_distance": 2,
                            "time_headway": 0.7,
                            "comfortable_deceleration": 1.5
                        }),
                        3000),
                    (ProportionalIntegralControllerModule(
                        **{
                            "max_acceleration": 1,
                            "max_deceleration": 1.5,
                            "v_catch": 1,
                            "gu": 30,
                            "gl": 7,
                            "gamma": 2
                        }),
                        3000)),
                "awareness": 5,
                "comfortable_deceleration": 1.5,
                "reaction_time": 0.5,
                "relative_distance_error": 0.05,
                "inverse_average_estimation_error": 0.01
            }
            if n == 0 else None for n in range(vehicle_number)])

    print(std_dev_velocity)
    print(throughput)


simulation_0()
simulation_1()
simulation_2()
