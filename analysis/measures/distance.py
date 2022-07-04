import pandas as pd


def distance(position_df: pd.DataFrame, start_step: int = 0, end_step: int = None,
             looped: bool = False, road_length: int = 100):
    if end_step is None:
        end_step = len(position_df)
    vehicle_number = len(position_df.columns)

    if not looped:
        names = [f'From {i + 1} to {i + 2}' for i in range(vehicle_number)]
        distance_df = pd.DataFrame({names[i]: position_df.iloc[:, i] - position_df.iloc[:, i+1] for i in range(
            vehicle_number-1)})
    else:
        names = [f'From {i + 1} to {(i + 1) % vehicle_number + 1}' for i in range(vehicle_number)]
        distance_df = pd.DataFrame({names[i]: (position_df.iloc[:, i] - position_df.iloc[:, (i+1) % vehicle_number])
                                    % road_length for i in range(vehicle_number)})
    return distance_df[start_step:end_step]


def distance_std(position_df: pd.DataFrame, start_step: int = 0, end_step: int = None,
             looped: bool = False, road_length: int = 100):
    df = distance(position_df, start_step, end_step, looped, road_length)

    std_df = df.std(axis=0)
    return std_df




