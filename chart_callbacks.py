import pandas as pd
import plotly.graph_objects as go
import numpy as np
from pathlib import Path





def create_x_axis(df: pd.DataFrame, x_axis_length: int = 25) -> pd.DataFrame:
    """  This is the function that controles the horizontal range of the graphs
    TODO: this needs to be modified in the gui with a slider
    """
    df = df.head(x_axis_length).copy()
    df["X"] = range(len(df))
    return df

def format_x_axis(fig: go.Figure, df: pd.DataFrame) -> None:
    """ This is just hear to update the x value and refactor it out of the render_functions"""
    fig.update_xaxes(
        tickmode="array",
        tickvals=df["X"],
        ticktext=df["Timestamp"].dt.strftime("%H:%M"),
        title="Time in minutes",
        rangeslider_visible=False,
    )


def clean_price_data(df: pd.DataFrame) -> pd.DataFrame:
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%Y-%m-%d %H:%M', errors='coerce')
    df=df.dropna(subset=['Timestamp'])
    return df

def renderSimpleCandlestick(df: pd.DataFrame) -> Path:
    df = create_x_axis(df)
    fig = go.Figure(data=[go.Candlestick(
        x=df["X"],
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'])])

    format_x_axis(fig, df)

    fig.update_layout(
        height=900,
        title="Simple CandleStick Chart"
    )

    fig.write_html("Simple_Candlestick_chart.html")
    html_path = Path.cwd() / "Simple_Candlestick_chart.html"
    return html_path


def calcSimpleCandlestick(df: pd.DataFrame) -> pd.DataFrame:
    return df


def renderHeikin_ashi(df: pd.DataFrame) -> Path:
    df = create_x_axis(df)

    fig = go.Figure(data=[go.Candlestick(
        x=df['Timestamp'],
        open=df['HA_Open'],
        high=df['HA_High'],
        low=df['HA_Low'],
        close=df['HA_Close'])])

    format_x_axis(fig, df)

    fig.update_layout(
        height=900,
        title="Heikin Ashi Candlestick Chart"
    )
    fig.write_html("Heikin_Ashi_Candlestick_Chart.html")
    html_path = Path.cwd() / "Heikin_Ashi_Candlestick_Chart.html"
    return html_path

def calcHeikin_ashi(df: pd.DataFrame) -> pd.DataFrame:
    ha_df = df.copy()
    # 1 Calculate Close first (straght forward average)
    ha_df['HA_Close'] = (df['Open'] + df['High'] + df['Low'] + df['Close']) / 4
    # 2 Calculate open
    ha_open = np.zeros(len(df))
    ha_open[0] = df['Open'].iloc[0]

    for i in range(1, len(df)):
        ha_open[i] = (ha_open[i-1] + ha_df['HA_Close'].iloc[i-1]) /2
    ha_df['HA_Open'] = ha_open

    # Calculate High and Low using the new open and close bounds
    ha_df['HA_High'] = ha_df[['High', 'HA_Open', 'HA_Close']].max(axis=1)
    ha_df['HA_Low'] = ha_df[['Low', 'HA_Open', 'HA_Close']].min(axis=1)
    return ha_df

def render_ohlc(df: pd.DataFrame) -> Path:

    df = create_x_axis(df)

    fig = go.Figure(data=[go.Ohlc(
        x=df['Timestamp'],
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'])])

    fig.update_layout(
        height=900,
        title="Open High and Low Close Chart"
    )

    format_x_axis(fig, df)
    fig.write_html("Open_High_and_Low_Close_Chart.html")
    html_path = Path.cwd() / "Open_High_and_Low_Close_Chart.html"
    return html_path

def calc_ohlc(df: pd.DataFrame) -> pd.DataFrame:
    return df

def render_line(df: pd.DataFrame) -> Path:
    fig = go.Figure(data=[go.Scatter(
        x=df['Timestamp'],
        y=df['Close'],
        mode='lines')])

    fig.update_layout(
        xaxis=dict(
            rangeslider=dict(visible=False)),
        height=900,
        title="Line"
    )
    fig.write_html("Line.html")
    html_path = Path.cwd() / "Line.html"
    return html_path

def calc_line(df: pd.DataFrame) -> pd.DataFrame:
    return df

render_chart_handlers = {
    "Simple Candlestick": renderSimpleCandlestick,
    "OHLC" : render_ohlc,
    "Line" : render_line,
    #"Point & Figure": renderPointAndFigure,
    "Heikin Ashi": renderHeikin_ashi,
}

calc_chart_handlers = {
    "Simple Candlestick": calcSimpleCandlestick,
    "OHLC" : calc_ohlc,
    "Line" : calc_line,
    #"Point & Figure": calcPointAndFigure,
    "Heikin Ashi": calcHeikin_ashi,
}

