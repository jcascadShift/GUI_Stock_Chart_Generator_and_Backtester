import pandas as pd
import plotly.graph_objects as go
import tkinter as tk
from tkinterweb import HtmlFrame
from datetime import datetime
from loadandlabelcsvdata import loadcsv
from calculate_heikin_ashi import calculate_heikin_ashi
from pathlib import Path


"""
This is the section that loads the data and converts it to a data frame
The data is also modified to use the Heikin_ashi candlestick  instead of a regular one
"""
df = loadcsv()
df_ha = calculate_heikin_ashi(df)
df_ha['Timestamp'] = pd.to_datetime(df_ha['Timestamp'], format='%Y-%m-%d %H:%M', errors='coerce')
df_ha = df_ha.dropna(subset=['Timestamp'])
df_ha = df_ha.head(100)

"""
This section is where the data from the data frame is used to populate a plotly candlestick graph
"""

fig = go.Figure(data=[go.Candlestick(
    x=df_ha['Timestamp'],
    open=df_ha['HA_Open'],
    high=df_ha['HA_High'],
    low=df_ha['HA_Low'],
    close=df_ha['HA_Close'])])

fig.update_layout(
    xaxis=dict(
        rangeslider=dict(visible=False)
    ),
    height=650,
    title="Heikin Ashi Candlestick Chart"
)

fig.write_html("heikin_ashi_chart.html")
# after writing an html file it is then loaded into tkinterweb
html_path = Path.cwd() / "heikin_ashi_chart.html"

chart_url = html_path.as_uri()

root = tk.Tk()
frame = HtmlFrame(root, messages_enabled=True)
frame.load_file(chart_url)
frame.pack(fill="both",expand=True)

root.mainloop()
