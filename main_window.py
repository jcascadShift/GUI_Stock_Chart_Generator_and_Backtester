from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QPushButton,
    QVBoxLayout,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Heikin-Ashi Chart Generator") 
        self.resize(500, 300)

        self.open_chart_button = QPushButton("Open Chart")
        self.open_chart_button.clicked.connect(self.open_chart_window)

        central_widget = QWidget()
        layout = QVBoxLayout()

        self.open_chart_button.clicked.connect(self.open_chart_window)
        layout.addWidget(self.open_chart_button)
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

    def open_chart_window(self):
        print("Open chart button clicked")


