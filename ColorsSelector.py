# This Python file uses the following encoding: utf-8
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QSpacerItem
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPaintEvent
from PySide6.QtGui import QMouseEvent
from PySide6.QtGui import QPainter
from PySide6.QtGui import QBrush
from PySide6.QtGui import QColor
from PySide6.QtCore import Signal
from PySide6.QtCore import Slot
from PySide6.QtCore import QPoint
from PySide6.QtCore import QSize
from PySide6.QtCore import QRect
from PySide6.QtCore import Qt


class ColorTile(QWidget):
    __color: QColor = QColor()
    clickedLeft: Signal = Signal(QColor)
    clickedRight: Signal = Signal(QColor)

    def __init__(self, color: QColor = QColor(), parent=None):
        super().__init__(parent)
        self.__color = color
        self.setMinimumSize(QSize(15, 15))

    def color(self):
        return self.__color

    @Slot(QColor)
    def setColor(self, color: QColor):
        self.__color = color
        self.update()

    def paintEvent(self, event: QPaintEvent):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setBrush(QBrush(self.__color))
        painter.drawRect(QRect(QPoint(0, 0), self.size()))

    def mousePressEvent(self, event: QMouseEvent):
        super().mousePressEvent(event)
        if event.button() == Qt.MouseButton.LeftButton:
            self.clickedLeft.emit(self.__color)
        elif event.button() == Qt.MouseButton.RightButton:
            self.clickedRight.emit(self.__color)


class CurrentColorsSelector(QWidget):
    __pen_color_tile: ColorTile
    __brush_color_tile: ColorTile
    pen_color_changed: Signal = Signal(QColor)
    brush_color_changed: Signal = Signal(QColor)

    def __init__(self, colors: list = [], parent=None):
        super().__init__(parent)
        self.__pen_color_tile = ColorTile()
        self.__brush_color_tile = ColorTile()
        current_color_layout = QVBoxLayout()
        current_color_layout.addWidget(self.__pen_color_tile)
        current_color_layout.addWidget(self.__brush_color_tile)

        select_color_layout = QGridLayout()
        for index in range(len(colors)):
            tile = ColorTile(colors[index])
            tile.clickedLeft.connect(self.set_pen_color)
            tile.clickedRight.connect(self.set_brush_color)
            select_color_layout.addWidget(tile, index % 2, index / 2)

        layout = QHBoxLayout()
        layout.addLayout(current_color_layout, 0)
        layout.addSpacerItem(QSpacerItem(15, 0))
        layout.addLayout(select_color_layout, 0)
        layout.addStretch(1)# math.ceil(len(colors) / 2))
        self.setLayout(layout)

    @Slot(QColor)
    def set_pen_color(self, color: QColor):
        self.__pen_color_tile.setColor(color)
        self.pen_color_changed.emit(color)

    def pen_color(self):
        return self.__pen_color_tile.color()

    @Slot(QColor)
    def set_brush_color(self, color: QColor):
        self.__brush_color_tile.setColor(color)
        self.brush_color_changed.emit(color)

    def brush_color(self):
        return self.__brush_color_tile.color()
