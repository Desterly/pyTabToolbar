from typing import Optional, Union

from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QPainter, QPalette, QPixmap
from PyQt5.QtWidgets import (
    QProxyStyle,
    QStyle,
    QStyleOption,
    QStyleOptionComplex,
    QStyleOptionFocusRect,
    QStyleOptionToolButton,
    QWidget,
)


class TTToolButtonStyle(QProxyStyle):
    def __init__(self, base_style: Optional[QProxyStyle] = None, *args):
        super().__init__(*args)
        self._base_style = base_style or super()

    def drawControl(
        self,
        element: QStyle.ControlElement,
        opt: Union[QStyleOption, QStyleOptionToolButton],
        p: QPainter,
        widget: QWidget,
    ):
        if element == QStyle.CE_ToolButtonLabel:
            toolbutton = opt
            rect = toolbutton.rect
            shift_x = 0
            shift_y = 0
            if toolbutton.state & (QStyle.State_Sunken | QStyle.State_On):  # type: ignore
                shift_x = super(TTToolButtonStyle, self).pixelMetric(
                    QStyle.PM_ButtonShiftHorizontal, toolbutton, widget
                )
                shift_y = super(TTToolButtonStyle, self).pixelMetric(
                    QStyle.PM_ButtonShiftVertical, toolbutton, widget
                )
            has_arrow = bool(toolbutton.features & QStyleOptionToolButton.Arrow)  # type: ignore

            if (
                (not has_arrow and toolbutton.icon.isNull()) and toolbutton.text  # type: ignore
            ) or toolbutton.toolButtonStyle == QtCore.Qt.ToolButtonTextOnly:  # type: ignore
                alignment = (
                    QtCore.Qt.AlignTop
                    | QtCore.Qt.AlignHCenter
                    | QtCore.Qt.TextShowMnemonic
                )
                if not self.proxy().styleHint(QStyle.SH_UnderlineShortcut, opt, widget):
                    alignment |= QtCore.Qt.TextHideMnemonic
                rect.translate(shift_x, shift_y)
                p.setFont(toolbutton.font)  # type: ignore
                self.proxy().drawItemText(
                    p,
                    rect,
                    alignment,
                    toolbutton.palette,
                    bool(opt.state & QStyle.State_Enabled),  # type: ignore
                    toolbutton.text,  # type: ignore
                    QPalette.ButtonText,
                )
            else:
                pm = QPixmap()
                pm_size = toolbutton.iconSize  # type: ignore
                if not toolbutton.icon.isNull():  # type: ignore
                    state = (
                        QIcon.On if (toolbutton.state & QStyle.State_On) else QIcon.Off  # type: ignore
                    )
                    mode = QIcon().Mode
                    if not toolbutton.state & QStyle.State_Enabled:  # type: ignore
                        mode = QIcon.Disabled
                    elif (opt.state & QStyle.State_MouseOver) and (  # type: ignore
                        opt.state & QStyle.State_AutoRaise
                    ):
                        mode = QIcon.Active
                    else:
                        mode = QIcon.Normal
                    pm = toolbutton.icon.pixmap(  # type: ignore
                        toolbutton.rect.size().boundedTo(toolbutton.iconSize),  # type: ignore
                        mode,
                        state,
                    )

                    pm_size = pm.size()

                if toolbutton.toolButtonStyle != QtCore.Qt.ToolButtonIconOnly:  # type: ignore
                    p.setFont(toolbutton.font)  # type: ignore
                    pr = QtCore.QRect(rect)
                    tr = QtCore.QRect(rect)
                    alignment = QtCore.Qt.TextShowMnemonic
                    if not self.proxy().styleHint(
                        QStyle.SH_UnderlineShortcut, opt, widget
                    ):
                        alignment |= QtCore.Qt.TextHideMnemonic
                    if toolbutton.toolButtonStyle == QtCore.Qt.ToolButtonTextUnderIcon:  # type: ignore

                        pr.setHeight(pm_size.height() + 6)
                        tr.adjust(0, pr.height() - 1, 0, -2)
                        pr.translate(shift_x, shift_y)

                        if not has_arrow:
                            self.proxy().drawItemPixmap(
                                p,
                                pr,
                                int(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter),
                                pm,
                            )
                        alignment |= int(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)

                    else:
                        pr.setWidth(pm_size.width() + 8)
                        tr.adjust(pr.width(), 0, 0, 0)
                        pr.translate(shift_x, shift_y)
                        if not has_arrow:
                            self.proxy().drawItemPixmap(
                                p,
                                QStyle.visualRect(opt.direction, rect, pr),
                                QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter,
                                pm,
                            )
                        alignment |= int(QtCore.Qt.AlignTop) | int(
                            QtCore.Qt.AlignHCenter
                        )
                    tr.translate(shift_x, shift_y)
                    self.proxy().drawItemText(
                        p,
                        QStyle.visualRect(opt.direction, rect, tr),
                        alignment,
                        toolbutton.palette,
                        bool(toolbutton.state & QStyle.State_Enabled),  # type: ignore
                        toolbutton.text,  # type: ignore
                        QPalette.ButtonText,
                    )
                else:
                    rect.translate(shift_x, shift_y)

                    if not has_arrow:
                        self.proxy().drawItemPixmap(
                            p, rect, QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter, pm
                        )
            return
        super(TTToolButtonStyle, self).drawControl(element, opt, p, widget)

    def drawComplexControl(
        self,
        cc: QStyle.ComplexControl,
        opt: QStyleOptionComplex,
        p: QPainter,
        widget: QWidget,
    ):

        if cc == QStyle.CC_ToolButton:
            toolbutton = opt
            if toolbutton:
                button = super().subControlRect(
                    cc, toolbutton, QStyle.SC_ToolButton, widget
                )
                menuarea = super().subControlRect(
                    cc, toolbutton, QStyle.SC_ToolButtonMenu, widget
                )
                bflags = toolbutton.state & ~QStyle.State_Sunken  # type: ignore
                if bflags & QStyle.State_AutoRaise:
                    if not (bflags & QStyle.State_MouseOver) or (
                        not (bflags & QStyle.State_Enabled)
                    ):
                        bflags &= ~QStyle.State_Raised
                mflags = bflags
                if toolbutton.state & QStyle.State_Sunken:  # type: ignore
                    if toolbutton.activeSubControls & QStyle.SC_ToolButton:  # type: ignore
                        bflags |= QStyle.State_Sunken
                    mflags |= QStyle.State_Sunken

                tool = QStyleOption()
                tool.palette = toolbutton.palette
                if toolbutton.subControls & QStyle.SC_ToolButton:  # type: ignore
                    if bflags & (
                        QStyle.State_Sunken | QStyle.State_On | QStyle.State_Raised
                    ):
                        tool.rect = button
                        tool.state = bflags  # type: ignore
                        self.proxy().drawPrimitive(
                            QStyle.PE_PanelButtonTool, tool, p, widget
                        )
                if toolbutton.state & QStyle.State_HasFocus:  # type: ignore
                    fr = QStyleOptionFocusRect(toolbutton)  # type: ignore
                    fr.state = toolbutton.state
                    fr.direction = toolbutton.direction
                    fr.rect = QtCore.QRect(toolbutton.rect)
                    fr.fontMetrics = toolbutton.fontMetrics
                    fr.palette = toolbutton.palette
                    fr.rect.adjust(3, 3, -3, -3)
                    if toolbutton.features & QStyleOptionToolButton.MenuButtonPopup:  # type: ignore

                        fr.rect.adjust(
                            0,
                            0,
                            -self.proxy().pixelMetric(
                                QStyle.PM_MenuButtonIndicator, toolbutton, widget
                            ),
                            0,
                        )
                        self.proxy().drawPrimitive(
                            QStyle.PE_FrameFocusRect, fr, p, widget
                        )
                label = QStyleOptionToolButton(toolbutton)  # type: ignore
                label.state = bflags  # type: ignore
                fw = self.proxy().pixelMetric(QStyle.PM_DefaultFrameWidth, opt, widget)
                label.rect = button.adjusted(fw, fw, -fw, -fw)
                self.proxy().drawControl(QStyle.CE_ToolButtonLabel, label, p, widget)

                if toolbutton.subControls & QStyle.SC_ToolButtonMenu:  # type: ignore
                    tool.rect = menuarea
                    tool.state = mflags  # type: ignore
                    if mflags & (
                        QStyle.State_Sunken | QStyle.State_On | QStyle.State_Raised
                    ):
                        self.proxy().drawPrimitive(
                            QStyle.PE_IndicatorButtonDropDown, tool, p, widget
                        )
                    self.proxy().drawPrimitive(
                        QStyle.PE_IndicatorArrowDown, tool, p, widget
                    )
                elif toolbutton.features & QStyleOptionToolButton.HasMenu:  # type: ignore
                    mbi = self.proxy().pixelMetric(
                        QStyle.PM_MenuButtonIndicator, toolbutton, widget
                    )
                    ir = toolbutton.rect
                    new_toolbutton = toolbutton
                    new_toolbutton.rect = QtCore.QRect(
                        int(ir.center().x() + 1 - (mbi - 6) / 2),
                        ir.y() + ir.height() - mbi + 4,
                        mbi - 6,
                        mbi - 6,
                    )
                    self.proxy().drawPrimitive(
                        QStyle.PE_IndicatorArrowDown, new_toolbutton, p, widget
                    )
            return
        return super(TTToolButtonStyle, self).drawComplexControl(cc, opt, p, widget)
