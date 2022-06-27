import csv


def save_to_csv(road_data, simulation_name=""):
    with open(f'output/{simulation_name}_position.csv', 'w', newline='') as csvfile:
        data_writer = csv.writer(csvfile, delimiter=';')
        for line in range(road_data.age):
            data_writer.writerow(
                [road_data.vehicles_data[i][line].position for i in range(len(road_data.vehicles_data))])

    with open(f'output/{simulation_name}_velocity.csv', 'w', newline='') as csvfile:
        data_writer = csv.writer(csvfile, delimiter=';')
        for line in range(road_data.age):
            data_writer.writerow(
                [road_data.vehicles_data[i][line].velocity for i in range(len(road_data.vehicles_data))])

    with open(f'output/{simulation_name}_acceleration.csv', 'w', newline='') as csvfile:
        data_writer = csv.writer(csvfile, delimiter=';')
        for line in range(road_data.age):
            data_writer.writerow(
                [road_data.vehicles_data[i][line].acceleration for i in range(len(road_data.vehicles_data))])
