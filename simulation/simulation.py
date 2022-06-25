from .road import Road
from typing import Callable


class Simulation:
    road: Road
    name: str
    debug_function: Callable

    def __init__(self, name: str, debug_function: Callable = None, *args, **kwargs):
        self.name = name
        self.debug_function = debug_function
        self.road = Road(*args, **kwargs)

    def simulate(self, delta_time: float, time_steps: int):
        for t in range(time_steps):
            try:
                self.road.simulate_step(delta_time)
                if self.debug_function is not None:
                    self.debug_function(self.road, delta_time)
            except Exception as e:
                print(f"An error ocurred during the simulation!: {e}")
        self.road.data.save_to_csv(self.name)
