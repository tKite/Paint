# This Python file uses the following encoding: utf-8
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QResizeEvent
from PySide6.QtGui import QMouseEvent
from PySide6.QtGui import QPainter
from PySide6.QtGui import QImage
from PySide6.QtCore import QPoint
from PySide6.QtCore import QRect
from PySide6.QtCore import QSize
from PySide6.QtCore import Qt
from PaintTools import BasePaintTool


class DrawWindow(QWidget):
    image: QImage
    paint_tool: BasePaintTool = BasePaintTool()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.GlobalColor.white)
        self.setMinimumSize(QSize(1, 1))

    def paintEvent(self, event: QResizeEvent):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.drawImage(QRect(QPoint(0, 0), self.size()), self.image)
        self.paint_tool.draw(painter)

    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        self.image = self.image.scaled(event.size())

    def mousePressEvent(self, event: QMouseEvent):
        super().mousePressEvent(event)
        self.paint_tool.start(event.pos())
        self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        super().mouseReleaseEvent(event)
        self.paint_tool.finish(event.pos())
        self.update()

        painter = QPainter(self.image)
        self.paint_tool.draw(painter)

    def mouseMoveEvent(self, event: QMouseEvent):
        super().mouseMoveEvent(event)
        self.paint_tool.update(event.pos())
        self.update()
