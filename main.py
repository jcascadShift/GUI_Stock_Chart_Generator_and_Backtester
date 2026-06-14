import tkinter as tk
import calculate_heikin_ashi
from tkinterweb import HtmlFrame

fig = go.Figure(data=[go.Candlestick(
    x=df_ha['Date'],
    open=df_ha['HA_Open'],
    high=df_ha['HA_High'],
    low=df_ha['HA_Low'],
    close=df_ha['HA_Close'])



root = tk.Tk()
frame = HtmlFrame(root, messages_enabled=True)
frame.load_website(fig.show())
frame.pack(fill="both", expand=True)

root.mainloop()
