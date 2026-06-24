from pathlib import Path

from PyQt6.QtCore import QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QMainWindow

class ChartWindow(QMainWindow):
    def __init__(self, html_path: str | Path, chart_title: str):
        super().__init__()

        self.setWindowTitle(chart_title)
        self.web_view = QWebEngineView()
        self.setCentralWidget(self.web_view)

        html_path = Path(html_path).resolve()
        self.web_view.load(QUrl.fromLocalFile(str(html_path)))
        self.showMaximized()
