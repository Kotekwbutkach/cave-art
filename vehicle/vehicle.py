from .view_module import View, IntelligentDriverView, HumanDriverView
from .controller_module import Controller, IntelligentDriverController
from .physics_module import Physics
from data_structures.vehicle_data import VehicleData
from typing import List, Dict


class Vehicle:
    CURRENT_ID = 0
    id: int
    physics: Physics
    view: View
    controller: Controller
    history: VehicleData

    def __init__(self, physics: Physics, controller: Controller, view: View):
        Vehicle.CURRENT_ID += 1
        self.physics = physics
        self.controller = controller
        self.view = view
        self.history = VehicleData(self.physics.transform, Vehicle.CURRENT_ID)
        self.view.own_data = self.history

    def simulate_step(self, delta_time):
        information = self.view.get_information(delta_time)
        self.controller.update_information(information)
        acceleration_function = self.controller.acceleration_function()
        self.physics.simulate_step(acceleration_function, delta_time)

    def update_history(self):
        self.history.update()


def vehicle_factory(controller_name, view_name):
    def vehicle_maker(arglist: List[Dict]):
        controller: Controller
        view: View

        for i in range(len(arglist)):
            physics = Physics(**arglist[i])
            if controller_name == "IntelligentDriverController":
                controller = IntelligentDriverController(**arglist[i])
            else:
                controller = Controller()
            if view_name == "IntelligentDriverView":
                view = IntelligentDriverView(**arglist[i])
            elif view_name == "HumanDriverView":
                view = HumanDriverView(**arglist[i])
            else:
                view = View()
            yield Vehicle(physics, controller, view)
    return vehicle_maker


def produce_vehicles(controller_name, view_name, arglist):
    generator = vehicle_factory(controller_name, view_name)(arglist)
    return [v for v in generator]
