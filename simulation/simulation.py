from . import CircularRoad, Road
from vehicle import Vehicle
from typing import Callable, Dict, List
from analysis import to_csv, to_data_frame, velocity_std, throughput
from graphics import vehicle_plots, CircularRoadVisual, RoadVisual


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

    def __len__(self):
        return self.road.data.age

    def simulate(self, delta_time: float, time_steps: int):
        for t in range(time_steps):
            try:
                self.road.simulate_step(delta_time)
                if self.debug_function is not None:
                    self.debug_function(self.road, delta_time)
            except Exception as e:
                print(f"An error ocurred during the simulation!: {e}")
        to_csv(self.road.data, self.name)
        Vehicle.CURRENT_ID = 0

    def debug_simulate(self, delta_time: float, time_steps: int):
        for t in range(time_steps):
            self.road.simulate_step(delta_time)
            if self.debug_function is not None:
                self.debug_function(self.road, delta_time)
        to_csv(self.road.data, self.name)


def default_simulation(name, vehicle_number=15, road_length=260, simulation_length=10000, arglist: List[Dict] = None,
                       draw=False, show=False, analyze=False, circular=True, speed=3, screen_width=1000, screen_height=800):
    vehicle_parameters = [{"controller_module": "IntelligentDriverController",
                           "view_module": "HumanDriverView",
                           "position": road_length - (road_length*x) / vehicle_number,
                           "velocity": 0,
                           "acceleration": 0,
                           "vehicle_length": 5,
                           "awareness": 5,
                           "max_acceleration": 1,
                           "max_velocity": 25,
                           "minimum_distance": 4,
                           "time_headway": 2,
                           "comfortable_deceleration": 1.5,
                           "reaction_time": 1,
                           "relative_distance_error": 0.05,
                           "inverse_average_estimation_error": 0.01,
                           "correlation_times": 20}
                          for x in range(vehicle_number)]

    if arglist is not None:
        for vehicle_id in range(vehicle_number):
            if arglist[vehicle_id] is not None:
                for key in arglist[vehicle_id].keys():
                    vehicle_parameters[vehicle_id][key] = arglist[vehicle_id][key]

    sim = Simulation(name, circular=circular, length=road_length)
    sim.road.add_vehicles(vehicle_parameters)

    sim.debug_simulate(0.1, simulation_length)
    if draw:
        vehicle_plots(sim, sim.name + "_full", end=sim.road.data.age-45, show=show)
        vehicle_plots(sim, sim.name + "_pt1", end=1000, show=show)
        vehicle_plots(sim, sim.name + "_pt2", start=3000, end=4000, show=show)
        vehicle_plots(sim, sim.name + "_pt3", start=7000, end=8000, show=show)
    if show:
        if circular:
            vis = CircularRoadVisual(sim.road, speed=speed, screen_width=screen_width, screen_height=screen_height)
        else:
            vis = RoadVisual(sim.road, speed=speed, screen_width=screen_width, screen_height=screen_height)
    if analyze:
        pos_df, vel_df, acc_df = to_data_frame(sim.road.data)
        std = velocity_std(vel_df)
        thr = throughput(vel_df, road_length=road_length)
        return sim, (std, thr)

    return sim, None
