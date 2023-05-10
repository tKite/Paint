# This Python file uses the following encoding: utf-8
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import QMenuBar
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPixmap
from PySide6.QtGui import QImage
from PySide6.QtGui import QColor
from DrawWindow import DrawWindow
from PaintTools import BasePaintTool
from PaintTools import *
from ToolSelector import ToolSelector
from ColorsSelector import *


class MainWindow(QMainWindow):
    color_selector: CurrentColorsSelector
    tool_selector: ToolSelector
    draw_window: DrawWindow

    def __init__(self, parent=None):
        super().__init__(parent)

        self.tool_selector = ToolSelector(dict({
            "R": PaintRectTool(),
            "E": PaintEllipseTool(),
            "L": PaintLineTool(),
            "C": PaintCurveLineTool()
        }))
        self.addToolBar(self.tool_selector)

        self.color_selector = CurrentColorsSelector([
            QColor(255, 255, 0),
            QColor(255, 255, 0),
            QColor(255, 0, 0),
            QColor(0, 255, 0),
            QColor(255, 0, 0),
            QColor(0, 255, 0),
            QColor(0, 255, 255)
        ])
        self.draw_window = DrawWindow()

        menu = self.menuBar()
        menu.addAction("Load").triggered.connect(self.load_image)
        menu.addAction("Save").triggered.connect(self.save_image)
        menu.addAction("Quit").triggered.connect(qApp.quit)


        content_view = QWidget()
        layout = QVBoxLayout()
        content_view.setLayout(layout)
        layout.addWidget(self.color_selector, 0)
        layout.addWidget(self.draw_window, 1)
        self.setCentralWidget(content_view)

        self.tool_selector.tool_changed.connect(self.sync_tool_and_color)
        self.color_selector.pen_color_changed.connect(self.sync_tool_and_color)
        self.color_selector.brush_color_changed.connect(self.sync_tool_and_color)
        self.sync_tool_and_color()

    def sync_tool_and_color(self):
        current = self.tool_selector.current()
        current.pen_color = self.color_selector.pen_color()
        current.brush_color = self.color_selector.brush_color()
        self.draw_window.paint_tool = current

    def load_image(self):
        file = QFileDialog.getOpenFileName(self, "Load File", "", "Images (*.png *.xpm *.jpg)")[0]
        self.draw_window.image = QImage(file)
        self.draw_window.update()

    def save_image(self):
        file = QFileDialog.getSaveFileName(self, "Save File", "", "Images (*.png *.xpm *.jpg)")[0]
        self.draw_window.image.save(file, "PNG")


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
