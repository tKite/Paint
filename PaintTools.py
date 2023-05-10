# This Python file uses the following encoding: utf-8
from PySide6.QtGui import QPainter
from PySide6.QtGui import QBrush
from PySide6.QtGui import QColor
from PySide6.QtGui import QPen
from PySide6.QtCore import QPoint
from PySide6.QtCore import QRect
from PySide6.QtCore import Qt


class BasePaintTool:
    pen_color: QColor = Qt.GlobalColor.black
    brush_color: QColor = Qt.GlobalColor.yellow

    def __init__(self):
        pass

    def draw(self, painter: QPainter) -> None:
        pass

    def start(self, point: QPoint) -> None:
        pass

    def update(self, point: QPoint) -> None:
        pass

    def finish(self, point: QPoint) -> None:
        pass


class PaintRectTool(BasePaintTool):
    start_point: QPoint = QPoint()
    finish_point: QPoint = QPoint()

    def __init__(self):
        super().__init__()

    def draw(self, painter: QPainter) -> None:
        painter.save()
        painter.setPen(QPen(self.pen_color))
        painter.setBrush(QBrush(self.brush_color))
        painter.drawRect(QRect(self.start_point, self.finish_point))
        painter.restore()

    def start(self, point: QPoint) -> None:
        self.start_point = self.finish_point = point

    def update(self, point: QPoint) -> None:
        self.finish_point = point

    def finish(self, point: QPoint) -> None:
        self.finish_point = point


class PaintEllipseTool(BasePaintTool):
    start_point: QPoint = QPoint()
    finish_point: QPoint = QPoint()

    def __init__(self):
        super().__init__()

    def draw(self, painter: QPainter) -> None:
        painter.save()
        painter.setPen(QPen(self.pen_color))
        painter.setBrush(QBrush(self.brush_color))
        painter.drawEllipse(QRect(self.start_point, self.finish_point))
        painter.restore()

    def start(self, point: QPoint) -> None:
        self.start_point = self.finish_point = point

    def update(self, point: QPoint) -> None:
        self.finish_point = point

    def finish(self, point: QPoint) -> None:
        self.finish_point = point


class PaintLineTool(BasePaintTool):
    start_point: QPoint = QPoint()
    finish_point: QPoint = QPoint()

    def __init__(self):
        super().__init__()

    def draw(self, painter: QPainter) -> None:
        painter.save()
        painter.setPen(QPen(self.pen_color))
        painter.setBrush(QBrush(self.brush_color))
        painter.drawLine(self.start_point, self.finish_point)
        painter.restore()

    def start(self, point: QPoint) -> None:
        self.start_point = self.finish_point = point

    def update(self, point: QPoint) -> None:
        self.finish_point = point

    def finish(self, point: QPoint) -> None:
        self.finish_point = point


class PaintCurveLineTool(BasePaintTool):
    points: list = []

    def __init__(self):
        super().__init__()

    def draw(self, painter: QPainter) -> None:
        painter.save()
        painter.setPen(QPen(self.pen_color))
        painter.setBrush(QBrush(self.brush_color))
        painter.drawPolyline(self.points)
        painter.restore()

    def start(self, point: QPoint) -> None:
        self.points.clear()
        self.points.append(point)

    def update(self, point: QPoint) -> None:
        self.points.append(point)

    def finish(self, point: QPoint) -> None:
        self.points.append(point)
