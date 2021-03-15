from PyQt5 import QtCore
from PyQt5.QtGui import QWheelEvent
from PyQt5.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QScrollArea,
    QSizePolicy,
    QSpacerItem,
    QWidget,
)

import pytabtoolbar.group as group
import pytabtoolbar.tabtoolbar as tabtoolbar


class TTScroller(QtCore.QObject):
    def __init__(self, parent: QtCore.QObject):
        super(TTScroller, self).__init__(parent)

    def eventFilter(self, watched: QtCore.QObject, event: QtCore.QEvent) -> bool:
        if event.type() == QtCore.QEvent.Wheel:
            scroll = QScrollArea(watched)
            wheel = QWheelEvent(event)
            scrollbar = scroll.horizontalScrollBar()
            scrollbar.setValue(int(scrollbar.value() - wheel.angleDelta().y() / 5))
            return True
        return super(TTScroller, self).eventFilter(watched, event)


class Page(QWidget):
    Hiding = QtCore.pyqtSignal(int)
    Showing = QtCore.pyqtSignal(int)

    def __init__(self, index: int, page_name: str, parent: QWidget = None):
        super(Page, self).__init__(parent)

        self.myIndex: int = index
        self.setObjectName(page_name)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.MinimumExpanding)
        self.setContentsMargins(0, 0, 0, 0)

        self.hboxlayout = QHBoxLayout(self)
        self.hboxlayout.setContentsMargins(0, 0, 0, 0)
        self.hboxlayout.setSpacing(0)
        self.setLayout(self.hboxlayout)

        scroll_area = QScrollArea(self)
        scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)

        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setFrameShadow(QFrame.Plain)
        scroll_area.setLineWidth(0)
        scroll_area.setWidgetResizable(True)
        scroll_area.installEventFilter(TTScroller(scroll_area))

        self.inner_area = QFrame()
        self.inner_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Ignored)
        self.inner_area.setProperty("TTPage", QtCore.QVariant(True))
        self.inner_area.setContentsMargins(0, 0, 0, 0)
        self.inner_area.setFrameShape(QFrame.Box)
        self.inner_area.setLineWidth(0)

        self.innerLayout = QHBoxLayout(self.inner_area)
        self.innerLayout.setContentsMargins(0, 0, 0, 0)
        self.innerLayout.setSpacing(2)
        self.inner_area.setLayout(self.innerLayout)

        spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.innerLayout.addItem(spacer)
        scroll_area.setWidget(self.inner_area)
        self.hboxlayout.addWidget(scroll_area)

    def add_group(self, name: str):
        grp = group.Group(name, self.inner_area)
        self.innerLayout.insertWidget(self.innerLayout.count() - 1, grp)
        parent_toolbar = tabtoolbar.find_tabtoolbar(self)  # type: ignore[attr-defined]
        if not parent_toolbar:
            raise Exception("Could not find Parent Tabtoolbar")

        parent_toolbar.adjust_verticalsize(grp.height())
        return grp

    def hide(self):
        self.Hiding.emit(self.myIndex)

    def show(self):
        self.Showing.emit(self.myIndex)
