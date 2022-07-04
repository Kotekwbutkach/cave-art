import pandas as pd


def velocity_mean(velocity_df: pd.DataFrame, start_step: int = 0, end_step: int = None):
    if end_step is None:
        end_step = len(velocity_df)

    df = velocity_df.iloc[start_step:end_step, :]
    mean = velocity_df.mean().mean()

    return mean


def velocity_std(velocity_df: pd.DataFrame, start_step: int = 0, end_step: int = None):
    if end_step is None:
        end_step = len(velocity_df)

    df = velocity_df.iloc[start_step:end_step, :]
    mean = velocity_mean(velocity_df, start_step, end_step)
    var_df = (velocity_df - mean) ** 2
    std_df = var_df.sum().sum()/(len(df) * len(df.columns) - 1)
    return std_df
