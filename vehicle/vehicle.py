from data_structures import Transform, VehicleData, RoadData
from .vehicle_module import ViewModule, HumanDriverViewModule, ProportionalIntegralViewModule,\
    ControllerModule, IntelligentDriverControllerModule, FollowerStopperControllerModule,\
    ProportionalIntegralControllerModule,\
    PhysicsModule
from typing import Dict, List


class Vehicle:
    data: VehicleData
    view: ViewModule
    controller: ControllerModule
    physics: PhysicsModule

    def __init__(self,
                 road_data: RoadData,
                 transform: Transform,
                 vehicle_length: float,
                 view: ViewModule,
                 controller: ControllerModule,
                 physics: PhysicsModule):
        if road_data.looped:
            modulo = road_data.road_length
        else:
            modulo = None
        self.data = VehicleData(len(road_data), transform, vehicle_length, modulo)
        self.view = view.assemble(self.data)
        self.controller = controller
        self.physics = physics.assemble(transform)

    def __repr__(self):
        return f"""{self.data}
{self.view}
{self.controller}
{self.physics}
"""

    def simulate_step(self, road_data, delta_time):
        self.view.get_view(road_data)
        own_data, distances_list = self.view.get_information(delta_time)
        acceleration_function = self.controller.acceleration_function()
        self.physics.simulate_step(acceleration_function, own_data, distances_list, delta_time)

    def update(self):
        self.data.update()

    @staticmethod
    def from_kwargs(road_data, **kwargs):
        transform = Transform(kwargs["position"],
                              kwargs["velocity"],
                              kwargs["acceleration"])

        vehicle_length = kwargs["vehicle_length"]

        physics = PhysicsModule(**kwargs)

        if kwargs["controller_module"] == "FollowerStopperController":
            controller = FollowerStopperControllerModule(**kwargs)
        elif kwargs["controller_module"] == "IntelligentDriverController":
            controller = IntelligentDriverControllerModule(**kwargs)
        elif kwargs["controller_module"] == "ProportionalIntegralController":
            # only compatible with the corresponding view
            controller = ProportionalIntegralControllerModule(**kwargs)
        else:
            controller = ControllerModule(**kwargs)

        if kwargs["view_module"] == "HumanDriverView":
            view = HumanDriverViewModule(**kwargs)
        elif kwargs["view_module"] == "ProportionalIntegralView":
            # only compatible with the corresponding controller
            view = ProportionalIntegralViewModule(**kwargs)
        else:
            view = ViewModule(**kwargs)
        return Vehicle(road_data, transform, vehicle_length, view, controller, physics)

    @staticmethod
    def generate_vehicles(road_data, arglist: List[Dict]):
        for i in range(len(arglist)):
            yield Vehicle.from_kwargs(road_data, **arglist[i])

    @staticmethod
    def produce_vehicles(road_data, arglist: List[Dict]):
        return [v for v in Vehicle.generate_vehicles(road_data, arglist)]
