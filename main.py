import tkinter as tk
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from loadandlabelcsvdata import loadcsv
from calculate_heikin_ashi import calculate_heikin_ashi
from tkinterweb import HtmlFrame

df = loadcsv()
df_ha = calculate_heikin_ashi(df)
df_ha['Timestamp'] = pd.to_datetime(df_ha['Timestamp'], format='%Y-%m-%d %H:%M', errors='coerce')
df_ha = df_ha.dropna(subset=['Timestamp'])
df_ha = df_ha.head(100)

fig = go.Figure(data=[go.Candlestick(
    x=df_ha['Timestamp'],
    open=df_ha['HA_Open'],
    high=df_ha['HA_High'],
    low=df_ha['HA_Low'],
    close=df_ha['HA_Close'])])


root = tk.Tk()
root.geometry("1000x600")
root.title("Heikin Ashi Candlestick Chart")

frame = HtmlFrame(root, messages_enabled=True)
frame.pack(fill="both", expand=True)

chart_html = fig.to_html(include_plotlyjs='cdn')

frame.load_html(chart_html)

root.mainloop()
