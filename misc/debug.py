
DEBUG_TIMER = 0
DATA = dict()


def awareness_check(road):
    for v in road.vehicles:
        print(v.data.vehicle_id)
        print([w.vehicle_id for w in v.view.other_data_list])


def debug_function(road, delta_time):
    # awareness_check(road)

    global DEBUG_TIMER
    DEBUG_TIMER += 1
    print(DEBUG_TIMER)
