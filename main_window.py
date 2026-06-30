from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QLabel,
    QSlider,
    QMessageBox
)

from PyQt6.QtCore import Qt
from pathlib import Path
from chart_window import ChartWindow
from chart_callbacks import (
    render_chart_handlers,
    calc_chart_handlers,
    clean_price_data,
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
            "Point & Figure",
        ])



        self.open_chart_button = QPushButton("Open Chart")
        self.open_chart_button.clicked.connect(self.open_chart_window)
        self.chart_window = None
        central_widget = QWidget()

        #slider labels 
        self.slider_title = QLabel("chart width")
        self.slider_value_label = QLabel("25")
        self.help_button = QPushButton("?")
        value_layout = QHBoxLayout()
        value_layout.addWidget(self.slider_value_label)
        value_layout.addWidget(self.help_button)
        value_layout.addStretch()



        self.slider_warning_label= QLabel("Warning increasing the slider values will distort the graph and cause lag")
        #slider
        self.chart_width_slider = QSlider(Qt.Orientation.Horizontal)
        self.chart_width_slider.setMinimum(25)
        self.chart_width_slider.setMaximum(500)
        self.chart_width_slider.setTickInterval(25)
        self.chart_width_slider.setTickPosition(QSlider.TickPosition.TicksBelow)

        #binding connect for slider value
        
        self.chart_width_slider.valueChanged.connect(self.update_slider_label)

        #binding for the help button
        self.help_button.clicked.connect(self.show_chart_width_help)

        layout = QVBoxLayout()
        #button
        layout.addWidget(self.open_chart_button)
        #dropdown
        layout.addWidget(self.chart_selector)
        #slider
        layout.addWidget(self.slider_title)
        layout.addWidget(self.chart_width_slider)
        layout.addLayout(value_layout)
        layout.addWidget(self.slider_warning_label)
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

    def open_chart_window(self):
        chart_width = self.chart_width_slider.value()

        dfinit = loadcsv()
        dfclean = clean_price_data(dfinit)

        selected_chart = self.chart_selector.currentText()

        df = calc_chart_handlers[selected_chart](dfclean)
        #print(df[['Open','Close', 'HA_Open', 'HA_Close']].head(10))

        html_path = render_chart_handlers[selected_chart](df, chart_width)

        self.chart_window = ChartWindow(html_path, selected_chart)
        self.chart_window.show()


    def update_slider_label(self, value: int):
        value = round(value / 25) * 25
        self.chart_width_slider.setValue(value)
        self.slider_value_label.setText(str(value))

    def show_chart_width_help(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Chart Width")
        msg.setText(
            "The 25 represents the x axis of graph \n"
            "For most charts this Represents 25 minutes of time\n"
            "For Point And Figure charts this represents 25 columns \n"
        )
        msg.exec()


