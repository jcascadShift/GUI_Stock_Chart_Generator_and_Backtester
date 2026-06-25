from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QComboBox,
)
from pathlib import Path
from chart_window import ChartWindow
from chart_callbacks import (
    render_chart_handlers,
    calc_chart_handlers,
)
from loadandlabelcsvdata import loadcsv



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Menu")
        self.resize(500, 300)

        self.chart_selector = QComboBox()
        self.chart_selector.addItems([
            "Simple Candlestick",
            "Heikin Ashi",
            "OHLC",
            "Line",
        ])



        self.open_chart_button = QPushButton("Open Chart")
        self.open_chart_button.clicked.connect(self.open_chart_window)
        self.chart_window = None
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.chart_selector)
        layout.addWidget(self.open_chart_button)
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

    def open_chart_window(self):

        dfinit = loadcsv()

        selected_chart = self.chart_selector.currentText()

        df = calc_chart_handlers[selected_chart](dfinit)
        #print(df[['Open','Close', 'HA_Open', 'HA_Close']].head(10))


        html_path = render_chart_handlers[selected_chart](df)

        self.chart_window = ChartWindow(html_path, selected_chart)
        self.chart_window.show()



