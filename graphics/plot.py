import matplotlib.pyplot as plt
from .color import from_id


def vehicle_plots(simulation, start: int = 0, end: int = None):
    if end is None:
        end = simulation.road.data.age
    else:
        end = min(end, simulation.road.data.age)

    for vehicle_data in simulation.road.data.vehicles_data:
        plt.plot(list(range(start, end)), [transform.position for transform in vehicle_data[start:end]],
                 ",", color=from_id(vehicle_data.vehicle_id, sat=0.75))
    plt.savefig(f"graphs/{simulation.name}_position.png", format="png")
    plt.show()

    for vehicle_data in simulation.road.data.vehicles_data:
        plt.plot(list(range(start, end)), [transform.velocity for transform in vehicle_data[start:end]],
                 ",", color=from_id(vehicle_data.vehicle_id, sat=0.75))
    plt.savefig(f"graphs/{simulation.name}_velocity.png", format="png")
    plt.show()

    for vehicle_data in simulation.road.data.vehicles_data:
        plt.plot(list(range(start, end)), [transform.acceleration for transform in vehicle_data[start:end]],
                 ",", color=from_id(vehicle_data.vehicle_id, sat=0.75))
    plt.savefig(f"graphs/{simulation.name}_acceleration.png", format="png")
    plt.show()