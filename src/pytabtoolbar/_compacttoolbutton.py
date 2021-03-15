from typing import Union

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (
    QAction,
    QBoxLayout,
    QFrame,
    QMenu,
    QSizePolicy,
    QStyle,
    QStyleOptionToolButton,
    QStylePainter,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from pytabtoolbar.style import get_pixelmetric, get_scalefactor, TTToolButtonStyle


class _CompactToolButton(QFrame):
    def __init__(self, action: QAction, menu: QMenu, parent):
        super(_CompactToolButton, self).__init__(parent)
        self.overlay = _TTOverlayToolButton(self)

        iconsize = int(get_pixelmetric(QStyle.PM_LargeIconSize) * get_scalefactor(self))
        self.upButton = QToolButton(self)
        self.upButton.setProperty("TTInternal", QtCore.QVariant(True))
        self.upButton.setAutoRaise(True)
        self.upButton.setDefaultAction(action)
        self.upButton.setIconSize(QtCore.QSize(iconsize, iconsize))
        self.upButton.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self.upButton.setStyle(TTToolButtonStyle())
        self.upButton.setMaximumHeight(iconsize + 5)

        self.vlayout = QVBoxLayout(self)
        self.vlayout.setContentsMargins(0, 0, 0, 0)
        self.vlayout.setSpacing(0)
        self.vlayout.setDirection(QBoxLayout.TopToBottom)

        self.upButton.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.upButton.setPopupMode(QToolButton.DelayedPopup)
        self.vlayout.addWidget(self.upButton)

        self.downButton = QToolButton(self)
        self.downButton.setProperty("TTInternal", QtCore.QVariant(True))
        self.downButton.setAutoRaise(True)
        self.downButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.downButton.setPopupMode(QToolButton.InstantPopup)
        self.downButton.setMinimumHeight(25)
        self.downButton.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        self.downButton.setText(action.text())
        self.downButton.setToolTip(action.toolTip())
        self.downButton.setStyle(TTToolButtonStyle())

        if menu:
            self.downButton.setMenu(menu)
            menu.aboutToHide.connect(lambda: self.set_hover(False))

        self.vlayout.addWidget(self.downButton)
        self.setLayout(self.vlayout)

        self.hover = _TTHover(self, self.upButton, self.downButton)
        self.upButton.installEventFilter(self.hover)
        self.downButton.installEventFilter(self.hover)

    def set_hover(self, hover: bool):
        self.overlay.paint = hover
        self.update()


class _TTOverlayToolButton(QToolButton):
    def __init__(self, parent: QWidget):
        super(_TTOverlayToolButton, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        parent.installEventFilter(self)
        self.lower()
        self.paint = False

    def eventFilter(
        self, obj: QtCore.QObject, ev: Union[QtGui.QResizeEvent, QtCore.QEvent]
    ):
        if obj == self.parent():
            if ev.type() == QtCore.QEvent.Resize:
                self.resize(ev.size())  # type: ignore
            elif ev.type == QtCore.QEvent.ChildAdded:
                self.lower()
        return super(_TTOverlayToolButton, self).eventFilter(obj, ev)

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        if not self.paint:
            return

        sp = QStylePainter(self)
        opt = QStyleOptionToolButton()
        self.initStyleOption(opt)
        opt.state |= (
            QStyle.State_MouseOver | QStyle.State_AutoRaise | QStyle.State_Raised
        )  # type: ignore
        opt.activeSubControls |= QStyle.SC_ToolButton  # type: ignore
        sp.drawComplexControl(QStyle.CC_ToolButton, opt)


class _TTHover(QtCore.QObject):
    def __init__(self, parent: _CompactToolButton, up: QToolButton, down: QToolButton):
        super(_TTHover, self).__init__(parent)
        self.toolButton: _CompactToolButton = parent
        self.upButton: QToolButton = up
        self.downButton: QToolButton = down

    def eventFilter(self, watched: QtCore.QObject, event: QtCore.QEvent) -> bool:
        if event.type() == QtCore.QEvent.HoverLeave:
            self.toolButton.set_hover(False)
        elif event.type() == QtCore.QEvent.HoverEnter:
            if watched == self.upButton or watched == self.downButton:
                self.toolButton.set_hover(self.upButton.isEnabled())

        if watched == self.upButton:
            if event.type() == QtCore.QEvent.Hide:
                self.downButton.hide()
            elif event.type() == QtCore.QEvent.Show:
                self.downButton.show()
            elif event.type() == QtCore.QEvent.EnabledChange:
                self.downButton.setEnabled(self.upButton.isEnabled())
                self.toolButton.set_hover(
                    self.upButton.isEnabled() and self.upButton.underMouse()
                )
        return super(_TTHover, self).eventFilter(watched, event)
