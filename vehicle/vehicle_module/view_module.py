from data_structures.road_data import RoadData
from data_structures.vehicle_data import VehicleData
from typing import List


class ViewModule:
    awareness: int
    own_data: VehicleData
    other_data_list: List[VehicleData]

    def __init__(self, awareness, **kwargs):
        self.awareness = awareness

    def __repr__(self):
        return f"""ViewModule:
    awareness: {self.awareness}"""

    def get_view(self, road_data: RoadData):
        vehicle_id = self.own_data.vehicle_id
        if not road_data.looped:
            other_data_list = road_data.vehicles_data[road_data.active_index:vehicle_id]
        else:
            other_data_list = road_data.vehicles_data[vehicle_id+1:] + road_data.vehicles_data[:vehicle_id]
        self.other_data_list = other_data_list[-self.awareness:]

    def assemble(self, vehicle_data):
        self.own_data = vehicle_data
        return self

    def return_information(self):
        time = self.own_data.age() - 1
        return self.own_data[time],\
            [self.own_data.distance_at(vehicle_data, time) for vehicle_data in self.other_data_list]


class IntelligentDriverViewModule(ViewModule):
    pass


class HumanDriverViewModule(ViewModule):
    pass
