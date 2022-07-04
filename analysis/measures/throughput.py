import pandas as pd
from .velocity import velocity_mean


def throughput(velocity_df: pd.DataFrame, start_step: int = 0, end_step: int = None, road_length: int = 100):
    if end_step is None:
        end_step = len(velocity_df)

    df = velocity_df.iloc[start_step:end_step, :]
    vehicle_number = len(df.columns)

    mean = velocity_mean(velocity_df, start_step, end_step)
    return vehicle_number * mean / road_length
