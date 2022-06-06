import matplotlib.pyplot as plt


def full_road_info(road, delta_time):
    for vehicle in road.vehicles:
        print(f"Vehicle {vehicle.id}: {vehicle.history}")


DEBUG_TIMER = 0
DATA = dict()


def show_distance(road, delta_time):
    global DEBUG_TIMER
    global DATA
    if not DATA:
        for vehicle in road.vehicles:
            DATA[vehicle] = []

    for vehicle in road.vehicles:
        DATA[vehicle].append(vehicle.view.get_information(delta_time)[-1])

    if DEBUG_TIMER == 1000:
        for vehicle in road.vehicles:
            data = [d.position for d in DATA[vehicle]]
            plt.plot(data)
        plt.savefig("graphs/debug_distance.png", format="png")
        plt.show()
        for vehicle in road.vehicles:
            data = [d.velocity for d in DATA[vehicle]]
            plt.plot(data)
        plt.savefig("graphs/debug_velocity_diff.png", format="png")
        plt.show()
        for vehicle in road.vehicles:
            data = [d.acceleration for d in DATA[vehicle]]
            plt.plot(data)
        plt.savefig("graphs/debug_acceleration_diff.png", format="png")
        plt.show()


def show_acceleration_logic(road, delta_time):
    for vehicle in road.vehicles:
        print(vehicle.id)
        print(f"Total: {vehicle.controller.acceleration_function()()}")
        print(f"Free: {vehicle.controller.free_acceleration()}")
        print(f"Max_v: {vehicle.controller.max_velocity}")
        print(f"Current_v: {vehicle.controller.information[0].velocity}")
        print(f"View_v: {vehicle.view.own_data.velocity[-1]}")
        for i in range(1, len(vehicle.controller.information)):
            print(f"Braking {i}: {vehicle.controller.braking_interaction(i)}")


def show_delta_time_correctness(road, delta_time):
    if DEBUG_TIMER == 400:
        print(road.vehicles[0].view.own_data.position)
        print([road.vehicles[0].view.own_data.get_at(x).position for x in range(DEBUG_TIMER)])
        print([road.vehicles[0].view.own_data.get_at(x-0.5).position for x in range(DEBUG_TIMER)])


def debug_function(road, delta_time):
    show_distance(road, delta_time)
    show_delta_time_correctness(road, delta_time)
    # show_acceleration_logic(road, delta_time)

    global DEBUG_TIMER
    DEBUG_TIMER += 1
    print(DEBUG_TIMER)
