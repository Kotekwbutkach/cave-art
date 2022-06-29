from . import CircularRoad, Road
from vehicle import Vehicle
from typing import Callable, Dict, List
from analysis import save_to_csv
from graphics import vehicle_plots


class Simulation:
    road: Road
    name: str
    debug_function: Callable

    def __init__(self, name: str, circular: bool = False, debug_function: Callable = None, *args, **kwargs):
        self.name = name
        self.debug_function = debug_function
        if circular:
            self.road = CircularRoad(*args, **kwargs)
        else:
            self.road = Road(*args, **kwargs)

    def simulate(self, delta_time: float, time_steps: int):
        for t in range(time_steps):
            try:
                self.road.simulate_step(delta_time)
                if self.debug_function is not None:
                    self.debug_function(self.road, delta_time)
            except Exception as e:
                print(f"An error ocurred during the simulation!: {e}")
        save_to_csv(self.road.data, self.name)
        Vehicle.CURRENT_ID = 0

    def debug_simulate(self, delta_time: float, time_steps: int):
        for t in range(time_steps):
            self.road.simulate_step(delta_time)
            if self.debug_function is not None:
                self.debug_function(self.road, delta_time)
        save_to_csv(self.road.data, self.name)


def default_simulation(name, number=21, road_length=260, simulation_length=10000, arglist: List[Dict]=None, show=False):
    if arglist is None:
        arglist = dict()

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
                           "relative_distance_error": 0.05,
                           "inverse_average_estimation_error": 0.01,
                           "correlation_times": 20}
                          for x in range(number)]

    for vehicle_id in range(number):
        for key in arglist[vehicle_id].keys():
                vehicle_parameters[vehicle_id][key] = arglist[vehicle_id][key]

    sim = Simulation(name, circular=True, length=road_length)
    sim.road.add_vehicles(vehicle_parameters)

    sim.simulate(0.1, simulation_length)

    vehicle_plots(sim, end=sim.road.data.age-45, show=show)
    vehicle_plots(sim, sim.name + "_pt1", end=1000, show=show)
    vehicle_plots(sim, sim.name + "_pt2", start=3000, end=4000, show=show)
    vehicle_plots(sim, sim.name + "_pt3", start=6000, end=8000, show=show)

    return sim