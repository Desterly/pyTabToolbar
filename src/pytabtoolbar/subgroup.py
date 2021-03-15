from dataclasses import dataclass
from enum import Enum

from typing import List, Union

from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QAction,
    QBoxLayout,
    QFrame,
    QHBoxLayout,
    QMenu,
    QSizePolicy,
    QSpacerItem,
    QStyle,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

import pytabtoolbar.style as style

import pytabtoolbar.tabtoolbar as tabtoolbar


@dataclass
class ActionParams:
    type: Union[QToolButton.ToolButtonPopupMode, None] = None
    action: Union[QAction, None] = None
    menu: Union[QMenu, None] = None


class Align(Enum):
    No = 0
    Yes = 1


class SubGroup(QFrame):
    def __init__(self, align: Align, parent: QWidget):
        super(SubGroup, self).__init__(parent)
        self.setFrameShape(QFrame.NoFrame)
        self.setLineWidth(0)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self.innerLayout = QVBoxLayout(self)
        # self.innerLayout.setMargin(0)
        self.innerLayout.setContentsMargins(0, 0, 0, 0)
        self.innerLayout.setSpacing(1)
        self.innerLayout.setDirection(QBoxLayout.TopToBottom)
        spacer = QSpacerItem(
            0,
            0,
            QSizePolicy.MinimumExpanding,
            (QSizePolicy.Expanding if align == Align.Yes else QSizePolicy.Ignored),
        )
        self.innerLayout.addItem(spacer)
        self.setLayout(self.innerLayout)

    def construct_innerframe(self, spacing: int) -> QFrame:
        parent_toolbar = tabtoolbar.find_tabtoolbar(self)
        if not parent_toolbar:
            raise Exception("Could not find Parent Tabtoolbar")
        group_maxheight = parent_toolbar.group_maxheight
        rowcount = parent_toolbar.rowcount()
        frame = QFrame(self)
        frame.setFrameShape(QFrame.NoFrame)
        frame.setLineWidth(0)
        frame.setContentsMargins(0, 0, 0, 0)
        policy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        policy.setHorizontalStretch(0)
        policy.setVerticalStretch(1)
        frame.setSizePolicy(policy)
        frame.setMaximumHeight(group_maxheight / rowcount)
        llayout = QHBoxLayout(frame)
        # layout.setMargin(0)
        llayout.setContentsMargins(0, 0, 0, 0)
        llayout.setSpacing(spacing)
        llayout.setDirection(QBoxLayout.LeftToRight)
        frame.setLayout(llayout)
        spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        llayout.addItem(spacer)
        return frame

    def add_action(
        self, type: QToolButton.ToolButtonPopupMode, action: QAction, menu: QMenu
    ):
        iconsize = int(
            style.get_pixelmetric(QStyle.PM_SmallIconSize) * style.get_scalefactor(self)
        )

        frame = self.construct_innerframe(0)
        btn = QToolButton(self)
        btn.setProperty("TTInternal", QtCore.QVariant(True))
        btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        btn.setAutoRaise(True)
        btn.setDefaultAction(action)
        btn.setPopupMode(type)
        btn.setIconSize(QtCore.QSize(iconsize, iconsize))
        if menu:
            btn.setMenu(menu)
        btn.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        frame.layout().addWidget(btn)
        self.innerLayout.insertWidget(self.innerLayout.count() - 1, frame)

    def add_widget(self, widget: QWidget):
        frame = self.construct_innerframe(4)
        widget.setParent(frame)
        widget.setProperty("TTInternal", QtCore.QVariant(True))
        frame.layout().addWidget(widget)
        self.innerLayout.insertWidget(self.innerLayout.count() - 1, frame)

    def add_hbuttons(self, params: List[ActionParams]):
        iconsize = int(
            style.get_pixelmetric(QStyle.PM_SmallIconSize) * style.get_scalefactor(self)
        )
        frame = self.construct_innerframe(0)
        frame.setProperty("TTHorizontalFrame", QtCore.QVariant(True))
        for param in params:
            btn = QToolButton(self)
            btn.setProperty("TTInternal", QtCore.QVariant(True))
            btn.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
            btn.setAutoRaise(True)
            btn.setDefaultAction(param.action)
            btn.setPopupMode(param.type)
            btn.setIconSize(QtCore.QSize(iconsize, iconsize))
            if param.menu:
                btn.setMenu(param.menu)
            btn.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
            frame.layout().addWidget(btn)
        self.innerLayout.insertWidget(self.innerLayout.count() - 1, frame)
