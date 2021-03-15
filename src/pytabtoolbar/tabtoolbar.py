from typing import Union
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (
    QAction,
    QBoxLayout,
    QFrame,
    QHBoxLayout,
    QSizePolicy,
    QTabWidget,
    QToolBar,
    QToolButton,
    QWidget,
)

import pytabtoolbar.page as page
import pytabtoolbar.style as style


class TabToolbar(QToolBar):
    """[summary]

    Args:
        _TabToolbar ([type]): [description]

    Returns:
        [type]: [description]
    """

    Minimized = QtCore.pyqtSignal()
    Maximized = QtCore.pyqtSignal()
    SpecialTabClicked = QtCore.pyqtSignal()
    StyleChanged = QtCore.pyqtSignal()

    def __init__(
        self, parent: QWidget = None, group_maxheight: int = 75, group_rowcount: int = 3
    ):
        super(TabToolbar, self).__init__(parent)
        style.register_default_styles()
        self.group_rowcount = group_rowcount
        self.group_maxheight = group_maxheight
        self.has_specialtab = False
        self.current_index = 0
        self.ignore_styleevent = False
        self.is_shown = True
        self._is_minimized = False
        self.maxheight = QtWidgets.QWIDGETSIZE_MAX
        self._style = style.StyleParams()
        self.setObjectName("TabToolbar")

        # self.tempShowTimer = QtCore.QTimer()
        # self.tempShowTimer.setSingleShot(True)
        # self.tempShowTimer.setInterval(QApplication.doubleClickInterval())

        self.setProperty("TabToolbar", QtCore.QVariant(True))
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFloatable(False)
        self.setMovable(False)
        self.setAllowedAreas(QtCore.Qt.TopToolBarArea)
        self.tabBar = QTabWidget(self)

        self.tabBar.setProperty("TTWidget", QtCore.QVariant(True))
        self.tabBar.tabBar().setProperty("TTTab", QtCore.QVariant(True))
        self.tabBarHandle = self.addWidget(self.tabBar)
        self.tabBar.setUsesScrollButtons(True)

        self.cornerActions = QFrame(self)
        self.cornerActions.setFrameShape(QFrame.NoFrame)
        self.cornerActions.setLineWidth(0)
        self.cornerActions.setContentsMargins(0, 0, 0, 0)
        self.cornerActions.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        self.cornerLayout = QHBoxLayout(self.cornerActions)

        self.cornerLayout.setContentsMargins(0, 0, 0, 0)
        self.cornerLayout.setSpacing(0)
        self.cornerLayout.setDirection(QBoxLayout.LeftToRight)
        self.cornerActions.setLayout(self.cornerLayout)

        self.hideAction = QAction(self)
        self.hideAction.setCheckable(True)
        self.hideAction.setText("▲")
        self.hideButton = QToolButton(self.tabBar)
        self.hideButton.setProperty("TTHide", QtCore.QVariant(True))
        self.hideButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.hideButton.setDefaultAction(self.hideAction)
        self.hideButton.setAutoRaise(True)
        self.hideButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.hideAction.triggered.connect(self._hideaction)
        self.tabBar.tabBarDoubleClicked.connect(self.hideAction.trigger)
        self.tabBar.tabBarClicked.connect(self.current_tabchanged)
        self.tabBar.currentChanged.connect(self.focus_changed)
        self.cornerLayout.addWidget(self.hideButton)
        self.tabBar.setCornerWidget(self.cornerActions)
        self.set_style(style.get_defaultstyle())

    def _hideaction(self):
        # self.tempShowTimer.start()
        self._is_minimized = self.hideAction.isChecked()
        self.hideAction.setText("▼" if self._is_minimized else "▲")
        self.hide_at(self.tabBar.currentIndex())
        if self._is_minimized:
            self.Minimized.emit()
        else:
            self.Maximized.emit()

    def event(self, event: QtCore.QEvent):
        if event.type() == QtCore.QEvent.StyleChange and not self.ignore_styleevent:
            # TODO: Validatre if we need a timer
            stylename = (
                self._style.objectName() if self._style else style.get_defaultstyle()
            )
            self.set_style(stylename)
        return super(TabToolbar, self).event(event)

    def focus_changed(self, old: QWidget = None, now: QWidget = None):
        if now and now != self:
            if self.isMinimized() and self.is_shown:
                parent = now
                while parent:
                    parent = parent.parent()
                    if parent == self:
                        return
                self.hide_at(self.current_index)

    def rowcount(self):
        return self.group_rowcount

    def group_maxheight(self):
        return self.group_maxheight * style.get_scalefactor(self)

    def set_style(self, stylename: str):
        self.ignore_styleevent = True
        self._style = style.create_style(stylename)
        stylesheet = style.get_stylesheet(self._style)
        self.setStyleSheet(stylesheet)
        self.ignore_styleevent = False
        self.StyleChanged.emit()

    def get_style(self) -> str:
        if self._style:
            return self._style.objectName()
        return ""

    def add_corneraction(self, action: QAction):
        action_button = QToolButton(self.tabBar)
        action_button.setProperty("TTInternal", QtCore.QVariant(True))
        action_button.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        action_button.setDefaultAction(action)
        action_button.setAutoRaise(True)
        action_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.cornerActions.layout().addWidget(action_button)

    def set_specialtabenabled(self, enabled: bool):
        self.has_specialtab = enabled
        self.tabBar.tabBar().setProperty("TTSpecial", QtCore.QVariant(enabled))
        if enabled and self.tabBar.count() > 0:
            self.tabBar.setCurrentIndex(1)

    def hide_action(self) -> QAction:
        return self.hideAction

    def tab_clicked(self, index: int):
        if self.tempShowTimer.isActive() or (index == 0 and self.has_specialtab):
            return
        if self._is_minimized:
            if self.is_shown and index != self.current_index:
                return
            self._is_minimized = self.is_shown
            self.hide_at(index)
            self._is_minimized = True

    def current_tabchanged(self, index: int):
        QtCore.QSignalBlocker(self.tabBar)
        if index == 0 and self.has_specialtab:
            self.tabBar.setCurrentIndex(self.current_index)
            self.SpecialTabClicked.emit()
        else:
            self.current_index = index

    @property
    def current_tab(self) -> int:
        return self.current_index

    def set_currenttab(self, index: int):
        self.tabBar.setCurrentIndex(index)

    def hide_at(self, index: int):
        if self._is_minimized:
            minheight = self.tabBar.tabBar().height() + 2
            self.tabBar.setMaximumHeight(minheight)
            self.tabBar.setMinimumHeight(minheight)
            self.setMaximumHeight(minheight)
            self.setMinimumHeight(minheight)
            self.is_shown = False
        else:
            self.tabBar.setCurrentIndex(index)
            if not self.is_shown:
                self.tabBar.setMaximumHeight(self.maxheight)
                self.tabBar.setMinimumHeight(self.maxheight)
                self.setMaximumHeight(self.maxheight)
                self.setMinimumHeight(self.maxheight)
                self.tabBar.adjustSize()
            self.setFocus()
            self.is_shown = True

    def hide_tab(self, index: int):
        page = self.sender()
        QtCore.QSignalBlocker(page)
        for i in range(self.tabBar.count()):
            if self.tabBar.widget(i) == page:
                self.tabBar.removeTab(i)
                return
        self.current_index = self.tabBar.currentIndex()

    @QtCore.pyqtSlot(int)
    def _adjustverticalsize(self, vsize: int):
        self.maxheight = vsize + self.tabBar.tabBar().height() + 6
        self.setMaximumHeight(self.maxheight)
        self.setMinimumHeight(self.maxheight)

    def adjust_verticalsize(self, vsize: int):
        QtCore.QTimer.singleShot(0, lambda: self._adjustverticalsize(vsize))  # type: ignore[attr-defined]
        # self._AdjustVerticleSize(vSize)

    def show_tab(self, index: int):
        tab_page = self.sender()
        QtCore.QSignalBlocker(tab_page)
        self.tabBar.insertTab(index, tab_page, tab_page.objectName())
        self.current_index = self.tabBar.currentIndex()

    def add_page(self, page_name: str) -> page.Page:
        tab_page = page.Page(self.tabBar.count(), page_name)
        QtCore.QSignalBlocker(tab_page)
        tab_page.Hiding.connect(self.hide_tab)
        tab_page.Showing.connect(self.show_tab)
        self.tabBar.addTab(tab_page, page_name)
        return tab_page


def find_tabtoolbar(starting_widget: QWidget) -> Union[TabToolbar, None]:
    par = starting_widget
    while par:
        if isinstance(par, TabToolbar):
            return par
        par = par.parent()
    return None
