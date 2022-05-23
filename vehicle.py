from view_module import View, IntelligentDriverView, HumanDriverView
from controller_module import Controller, IntelligentDriverController
from physics_module import Physics
from data_structures import TransformData
from typing import List, Dict


class Vehicle:
    physics: Physics
    view: View
    controller: Controller

    def __init__(self, physics: Physics, controller: Controller, view: View):
        self.physics = physics
        self.controller = controller
        self.view = view

        self.history = TransformData(self.physics.transform)
        self.view.own_data = self.history

    def simulate_step(self, delta_time):
        information = self.view.get_information(delta_time)
        self.controller.update_information(information)
        acceleration_function = self.controller.acceleration_function()
        self.physics.simulate_step(acceleration_function, delta_time)
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
            if view_name == "HumanDriverView":
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
