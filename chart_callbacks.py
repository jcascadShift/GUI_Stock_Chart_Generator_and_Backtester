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
    df = create_x_axis(df)

    fig = go.Figure(data=[go.Scatter(
        x=df['Timestamp'],
        y=df['Close'],
        mode='lines')])

    fig.update_layout(
        height=900,
        title="Line"
    )

    format_x_axis(fig, df)
    fig.write_html("Line.html")
    html_path = Path.cwd() / "Line.html"
    return html_path

def calc_line(df: pd.DataFrame) -> pd.DataFrame:
    return df

def calcPointAndFigure(
    df: pd.DataFrame,
    box_size: float = 0.0005,
    reversal_boxes: int = 3
) -> pd.DataFrame:
    """
    Convert regular OHLC/Close data into Point & Figure data.

    box_size:
        Size of one P&F box. For EUR/USD, 0.0005 = 5 pips.

    reversal_boxes:
        Number of boxes required to reverse direction.
        Common default is 3.
    """

    if df.empty:
        return pd.DataFrame(columns=["Column", "BoxPrice", "Symbol"])

    close_prices = df["Close"].dropna()

    if close_prices.empty:
        return pd.DataFrame(columns=["Column", "BoxPrice", "Symbol"])

    current_price = close_prices.iloc[0]
    last_box_price = round(current_price / box_size) * box_size

    direction = None
    column = 0
    points = []

    for price in close_prices.iloc[1:]:
        box_price = round(price / box_size) * box_size

        if direction is None:
            boxes_moved = int(round((box_price - last_box_price) / box_size))

            if boxes_moved > 0:
                direction = "X"
                for i in range(1, boxes_moved + 1):
                    points.append({
                        "Column": column,
                        "BoxPrice": last_box_price + i * box_size,
                        "Symbol": "X"
                    })
                last_box_price = last_box_price + boxes_moved * box_size

            elif boxes_moved < 0:
                direction = "O"
                for i in range(1, abs(boxes_moved) + 1):
                    points.append({
                        "Column": column,
                        "BoxPrice": last_box_price - i * box_size,
                        "Symbol": "O"
                    })
                last_box_price = last_box_price + boxes_moved * box_size

            continue

        if direction == "X":
            # Continue upward column
            if box_price > last_box_price:
                boxes_up = int(round((box_price - last_box_price) / box_size))

                for i in range(1, boxes_up + 1):
                    points.append({
                        "Column": column,
                        "BoxPrice": last_box_price + i * box_size,
                        "Symbol": "X"
                    })

                last_box_price = last_box_price + boxes_up * box_size

            # Reverse downward
            elif box_price <= last_box_price - reversal_boxes * box_size:
                column += 1
                direction = "O"

                boxes_down = int(round((last_box_price - box_price) / box_size))

                for i in range(1, boxes_down + 1):
                    points.append({
                        "Column": column,
                        "BoxPrice": last_box_price - i * box_size,
                        "Symbol": "O"
                    })

                last_box_price = last_box_price - boxes_down * box_size

        elif direction == "O":
            # Continue downward column
            if box_price < last_box_price:
                boxes_down = int(round((last_box_price - box_price) / box_size))

                for i in range(1, boxes_down + 1):
                    points.append({
                        "Column": column,
                        "BoxPrice": last_box_price - i * box_size,
                        "Symbol": "O"
                    })

                last_box_price = last_box_price - boxes_down * box_size

            # Reverse upward
            elif box_price >= last_box_price + reversal_boxes * box_size:
                column += 1
                direction = "X"

                boxes_up = int(round((box_price - last_box_price) / box_size))

                for i in range(1, boxes_up + 1):
                    points.append({
                        "Column": column,
                        "BoxPrice": last_box_price + i * box_size,
                        "Symbol": "X"
                    })

                last_box_price = last_box_price + boxes_up * box_size

    pnf_df = pd.DataFrame(points)

    if pnf_df.empty:
        return pd.DataFrame(columns=["Column", "BoxPrice", "Symbol"])

    pnf_df["X"] = pnf_df["Column"]

    return pnf_df

def create_point_figure_window(df: pd.DataFrame,visible_columns: int = 50) -> pd.DataFrame:
    max_column = df["X"].max()
    min_column = max_column - visible_columns + 1
    return df[df["X"] >= min_column].copy()


def renderPointAndFigure(df: pd.DataFrame) -> Path:

    #Do not include call to create_x_axis
    # point and figure charts work different x_axis is handled eslwhere
    fig = go.Figure()

    df = create_point_figure_window(df)

    fig.add_trace(
        go.Scatter(
            x=df["X"],
            y=df["BoxPrice"],
            mode="text",
            text=df["Symbol"],
            textfont=dict(
                size=18
            ),
            hoverinfo="skip"
        )
    )

    fig.update_layout(
        title="Point & Figure Chart",
        height=900,
        yaxis_title="Price"
    )
    fig.write_html("Point_and_Figure.html")
    html_path = Path.cwd() / "Point_and_Figure.html"
    return html_path

render_chart_handlers = {
    "Simple Candlestick": renderSimpleCandlestick,
    "OHLC" : render_ohlc,
    "Line" : render_line,
    "Point & Figure": renderPointAndFigure,
    "Heikin Ashi": renderHeikin_ashi,
}

calc_chart_handlers = {
    "Simple Candlestick": calcSimpleCandlestick,
    "OHLC" : calc_ohlc,
    "Line" : calc_line,
    "Point & Figure": calcPointAndFigure,
    "Heikin Ashi": calcHeikin_ashi,
}

