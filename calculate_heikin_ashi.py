import pandas as pd
import numpy as np


def calculate_heikin_ashi(df):
    ha_df = df.copy()
    # 1 Calculate Close first (stragiht forward average)
    ha_df['HA_Close'] = (df['Open'] + df['High'] + df['Low'] + df['Close']) / 4
    # 2 Calculate open
    ha_open = np.zeros(len(df))
    ha_open[0] = df['Open'].iloc[0]

    for i in range(1, len(df)):
        ha_open[i] = (ha_open[i-1] + ha_df['HA_Close'].iloc[i-1]) / 2

    ha_df['HA_Open'] = ha_open

    # Calculate High and low using the new open and close bounds
    ha_df['HA_High'] = ha_df[['High', 'HA_Open', 'HA_Close']].max(axis=1)
    ha_df['HA_Low'] = ha_df[['Low', 'HA_Open', 'HA_Close']].min(axis=1)

    return ha_df


