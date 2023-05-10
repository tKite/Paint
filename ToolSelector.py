# This Python file uses the following encoding: utf-8
from PySide6.QtWidgets import QButtonGroup
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QToolButton
from PySide6.QtWidgets import QToolBar
from PySide6.QtCore import Signal
from PaintTools import BasePaintTool


class ToolSelector(QToolBar):
    tool_changed: Signal = Signal()
    __tools: dict

    def __init__(self, tools: dict, parent=None):
        super().__init__(parent)

        self.__tools = tools
        layout = QHBoxLayout()
        self.group = QButtonGroup(self, exclusive=True)
        self.setLayout(layout)
        for tool_name, tool in self.__tools.items():
            button = QToolButton(text=tool_name, checkable=True)
            button.clicked.connect(lambda: self.tool_changed.emit())
            self.group.addButton(button)
            button.setChecked(True)
            self.addWidget(button)

    def current(self) -> BasePaintTool:
        return self.__tools[self.group.checkedButton().text()]
