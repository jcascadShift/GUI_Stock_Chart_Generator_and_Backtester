from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QPushButton,
    QVBoxLayout,
)
from pathlib import Path
from chart_window import ChartWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Heikin-Ashi Chart Generator") 
        self.resize(500, 300)

        self.open_chart_button = QPushButton("Open Chart")
        self.open_chart_button.clicked.connect(self.open_chart_window)
        self.chart_window = None
        central_widget = QWidget()
        layout = QVBoxLayout()

        self.open_chart_button.clicked.connect(self.open_chart_window)
        layout.addWidget(self.open_chart_button)
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

    def open_chart_window(self):
        html_path = Path.cwd() / "heikin_ashi_chart.html"

        self.chart_window = ChartWindow(html_path)
        self.chart_window.show()



