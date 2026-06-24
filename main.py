import sys
import pandas as pd
import plotly.graph_objects as go
from PyQt6.QtWidgets import QApplication
from main_window import MainWindow
from pathlib import Path
from chart_window import ChartWindow




# This launches the main window
app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())



