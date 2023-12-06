from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QAction,
    QBoxLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMenu,
    QSizePolicy,
    QStyle,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from ._compacttoolbutton import _CompactToolButton
import pytabtoolbar.style as style
import pytabtoolbar.subgroup as subgroup

# from .style import TTToolButtonStyle, get_pixelmetric, get_scalefactor
# from .subgroup import Align, SubGroup
import pytabtoolbar.tabtoolbar as tabtoolbar


class Group(QFrame):
    def __init__(self, name: str, parent: QWidget):
        super(Group, self).__init__(parent)
        # self.setFrameShape(QFrame.NoFrame)
        # self.setLineWidth(0)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)

        seperator_layout = QHBoxLayout(self)
        seperator_layout.setContentsMargins(0, 0, 0, 0)
        seperator_layout.setSpacing(0)
        seperator_layout.setDirection(QBoxLayout.LeftToRight)
        self.setLayout(seperator_layout)

        outer_layout = QVBoxLayout()
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)
        outer_layout.setDirection(QBoxLayout.TopToBottom)
        seperator_layout.addLayout(outer_layout)
        seperator_layout.addWidget(self.create_separator())

        inner_frame = QFrame(self)
        inner_frame.setFrameShape(QFrame.NoFrame)
        inner_frame.setLineWidth(0)
        inner_frame.setContentsMargins(0, 0, 0, 0)
        inner_frame.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.inner_layout = QHBoxLayout(inner_frame)
        self.inner_layout.setContentsMargins(2, 4, 2, 0)
        self.inner_layout.setSpacing(4)
        self.inner_layout.setDirection(QBoxLayout.LeftToRight)
        inner_frame.setLayout(self.inner_layout)

        outer_layout.addWidget(inner_frame)

        self.group_name = QLabel(name, self)
        self.group_name.setProperty("TTGroupName", QtCore.QVariant(True))
        self.group_name.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self.group_name.setAlignment(
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter  # type: ignore
        )
        self.group_name.adjustSize()
        outer_layout.addWidget(self.group_name)

        parent_tabtoolbar = tabtoolbar.find_tabtoolbar(self)
        if not parent_tabtoolbar:
            raise Exception("Could not find Parent Tabtoolbar")

        group_maxheight = parent_tabtoolbar.group_maxheight
        rowcount = parent_tabtoolbar.rowcount()
        height = group_maxheight + self.group_name.height() + rowcount - 1
        self.setMinimumHeight(height)
        self.setMaximumHeight(height)

    def add_subgroup(self, align: subgroup.Align) -> subgroup.SubGroup:
        sgrp = subgroup.SubGroup(align, self)
        self.inner_layout.addWidget(sgrp)
        return sgrp

    def create_separator(self) -> QFrame:
        separator = QFrame(self)
        separator.setProperty("TTSeparator", QtCore.QVariant(True))
        separator.setAutoFillBackground(False)
        separator.setFrameShadow(QFrame.Plain)
        separator.setLineWidth(1)
        separator.setMidLineWidth(0)
        separator.setFrameShape(QFrame.VLine)
        return separator

    def add_separator(self):
        self.inner_layout.addWidget(self.create_separator())

    def add_action(
        self, type: QToolButton.ToolButtonPopupMode, action: QAction, menu: QMenu
    ):
        if type == QToolButton.MenuButtonPopup:
            self.inner_layout.addWidget(_CompactToolButton(action, menu, self))
        else:
            icon_size = int(
                style.get_pixelmetric(QStyle.PM_LargeIconSize)
                * style.get_scalefactor(self)
            )

            btn = QToolButton(self)
            btn.setProperty("TTInternal", QtCore.QVariant(True))
            btn.setAutoRaise(True)
            btn.setDefaultAction(action)
            btn.setIconSize(QtCore.QSize(icon_size, icon_size))
            btn.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
            btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
            btn.setPopupMode(type)
            btn.setStyle(style.TTToolButtonStyle(self.inner_layout))
            if menu:
                btn.setMenu(menu)
            self.inner_layout.addWidget(btn)

    def add_widget(self, widget: QWidget):
        widget.setParent(self)
        widget.setProperty("TTInternal", QtCore.QVariant(True))
        self.inner_layout.addWidget(widget)
