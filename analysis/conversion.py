import pandas as pd
import csv
from data_structures import RoadData


def to_data_frame(road_data: RoadData):
    position_data = {f'Vehicle {i+1}': [v_data.position for v_data in road_data.vehicles_data[i]]
                     for i in range(len(road_data.vehicles_data))}
    position_df = pd.DataFrame(data=position_data)

    velocity_data = {f'Vehicle {i+1}': [v_data.velocity for v_data in road_data.vehicles_data[i]]
                     for i in range(len(road_data.vehicles_data))}
    velocity_df = pd.DataFrame(data=velocity_data)

    acceleration_data = {f'Vehicle {i+1}': [v_data.acceleration for v_data in road_data.vehicles_data[i]]
                         for i in range(len(road_data.vehicles_data))}
    acceleration_df = pd.DataFrame(data=acceleration_data)

    return position_df, velocity_df, acceleration_df


def to_csv(road_data, simulation_name=""):
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


def csv_to_data_frame(filepath: str):
    pos_df = pd.read_csv(f"{filepath}_position.csv", header=None, sep=";")
    vel_df = pd.read_csv(f"{filepath}_velocity.csv", header=None, sep=";")
    acc_df = pd.read_csv(f"{filepath}_acceleration.csv", header=None, sep=";")
    names = [f'Vehicle {i+1}' for i in range(len(pos_df.columns))]

    pos_df.columns = names
    vel_df.columns = names
    acc_df.columns = names

    return pos_df, vel_df, acc_df
