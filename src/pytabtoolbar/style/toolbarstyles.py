from sys import platform

from typing import Any, Dict, Final, List, Union

from PyQt5 import QtCore
from PyQt5.QtCore import (
    QT_VERSION_STR,
    QFile,
    QLocale,
    QObject,
    QPoint,
    QSysInfo,
    QVariant,
)
from PyQt5.QtGui import QColor, QGuiApplication, QPalette, QScreen
from PyQt5.QtWidgets import QApplication, QStyle, QWidget

from pytabtoolbar.style import styletemplate  # noqa
from pytabtoolbar.style.qtproperties import Property, PropertyMeta

STYLE_COOL: Final[str] = "Kool"
STYLE_VIENNA: Final[str] = "Vienna"
STYLE_THRESHOLD: Final[str] = "Threshold"
STYLE_WHITEMERCY: Final[str] = "White Mercy"


class Color:
    def __init__(self, coefficient: float, value: Union[QColor, QtCore.Qt.GlobalColor]):
        self.coefficient: float = coefficient
        if isinstance(value, QtCore.Qt.GlobalColor):
            self.value = QColor(value)
        else:
            self.value = value

    def __str__(self):
        return "Color(coefficient: {}, value: {}".format(self.coefficient, self.value)

    def __repr__(self):
        return self.__str__()


class Colors(QObject):
    def __init__(
        self,
        data: Union[QColor, QtCore.Qt.GlobalColor, List[Color]],
    ):
        self._list: List[Color] = []
        if data:
            if isinstance(data, QtCore.Qt.GlobalColor):
                self._list.append(Color(1.0, QColor(data)))
            elif isinstance(data, QColor):
                self._list.append(Color(1.0, data))
            elif isinstance(data, list):
                self._list = list(data)
            elif isinstance(data, Colors):
                self._list = list(data._items)
            else:
                raise Exception("Invalid type '{}' passed to Colors".format(type(data)))

        super(Colors, self).__init__()

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        if len(self._list) > 0:
            return self._list[0].value
        return None

    def __getitem__(self, item):
        return self._list[item]

    def __len__(self):
        return len(self._list)

    @property
    def _items(self):
        return self._list


class StyleParams(QObject, metaclass=PropertyMeta):
    AdditionalStyleSheet: str
    BorderColor = Property(QObject)
    GroupNameColor = Property(QObject)
    HideArrowColor = Property(QObject)
    HorizontalFrameBackgroundColor = Property(QObject)
    HorizontalFrameBorderColor = Property(QObject)
    HorizontalFrameBorderSize = Property(int)
    PaneColor = Property(QObject)
    SeparatorColor = Property(QObject)
    TabBorderRadius = Property(int)
    TabFontColor = Property(QObject)
    TabHoverBorderColorSide = Property(QObject)
    TabHoverBorderColorTop = Property(QObject)
    TabSelectedColor = Property(QObject)
    TabSpacing = Property(int)
    TabSpecialBorderColor = Property(QObject)
    TabSpecialBorderColorSide = Property(QObject)
    TabSpecialColor = Property(QObject)
    TabSpecialFontColor = Property(QObject)
    TabSpecialHoverBorderColor = Property(QObject)
    TabSpecialHoverBorderColorSide = Property(QObject)
    TabSpecialHoverColor = Property(QObject)
    TabUnselectedColor = Property(QObject)
    TabUnselectedHoverBorderColorSide = Property(QObject)
    TabUnselectedHoverBorderColorTop = Property(QObject)
    ToolbarBackgroundColor = Property(QObject)
    UseTemplateSheet: bool

    def __init__(self, parent=None):
        super().__init__(parent)
        self.AdditionalStyleSheet = ""
        self.BorderColor = None
        self.GroupNameColor = None
        self.HideArrowColor = None
        self.HorizontalFrameBackgroundColor = None
        self.HorizontalFrameBorderColor = None
        self.HorizontalFrameBorderSize = 0
        self.PaneColor = None
        self.SeparatorColor = None
        self.TabBorderRadius = 0
        self.TabFontColor = None
        self.TabHoverBorderColorSide = None
        self.TabHoverBorderColorTop = None
        self.TabSelectedColor = None
        self.TabSpacing = 0
        self.TabSpecialBorderColor = None
        self.TabSpecialBorderColorSide = None
        self.TabSpecialColor = None
        self.TabSpecialFontColor = None
        self.TabSpecialHoverBorderColor = None
        self.TabSpecialHoverBorderColorSide = None
        self.TabSpecialHoverColor = None
        self.TabUnselectedColor = None
        self.TabUnselectedHoverBorderColorSide = None
        self.TabUnselectedHoverBorderColorTop = None
        self.ToolbarBackgroundColor = None
        self.UseTemplateSheet = False

    def copy(self):
        new_style = StyleParams()
        new_style.AdditionalStyleSheet = str(self.AdditionalStyleSheet)
        new_style.BorderColor = Colors(self.BorderColor)
        new_style.GroupNameColor = Colors(self.GroupNameColor)
        new_style.HideArrowColor = Colors(self.HideArrowColor)
        new_style.HorizontalFrameBackgroundColor = Colors(
            self.HorizontalFrameBackgroundColor
        )
        new_style.HorizontalFrameBorderColor = Colors(self.HorizontalFrameBorderColor)
        new_style.HorizontalFrameBorderSize = int(self.HorizontalFrameBorderSize)
        new_style.PaneColor = Colors(self.PaneColor)
        new_style.SeparatorColor = Colors(self.SeparatorColor)
        new_style.TabBorderRadius = int(self.TabBorderRadius)
        new_style.TabFontColor = Colors(self.TabFontColor)
        new_style.TabHoverBorderColorSide = Colors(self.TabHoverBorderColorSide)
        new_style.TabHoverBorderColorTop = Colors(self.TabHoverBorderColorTop)
        new_style.TabSelectedColor = Colors(self.TabSelectedColor)
        new_style.TabSpacing = int(self.TabSpacing)
        new_style.TabSpecialBorderColor = Colors(self.TabSpecialBorderColor)
        new_style.TabSpecialBorderColorSide = Colors(self.TabSpecialBorderColorSide)
        new_style.TabSpecialColor = Colors(self.TabSpecialColor)
        new_style.TabSpecialFontColor = Colors(self.TabSpecialFontColor)
        new_style.TabSpecialHoverBorderColor = Colors(self.TabSpecialHoverBorderColor)
        new_style.TabSpecialHoverBorderColorSide = Colors(
            self.TabSpecialHoverBorderColorSide
        )
        new_style.TabSpecialHoverColor = Colors(self.TabSpecialHoverColor)
        new_style.TabUnselectedColor = Colors(self.TabUnselectedColor)
        new_style.TabUnselectedHoverBorderColorSide = Colors(
            self.TabUnselectedHoverBorderColorSide
        )
        new_style.TabUnselectedHoverBorderColorTop = Colors(
            self.TabUnselectedHoverBorderColorTop
        )
        new_style.ToolbarBackgroundColor = Colors(self.ToolbarBackgroundColor)
        new_style.UseTemplateSheet = bool(self.UseTemplateSheet)
        return new_style


class TPalette:
    def __init__(self):
        self.htext: QColor = QPalette().highlightedText().color()
        self.highlight: QColor = QPalette().highlight().color()
        self.light: QColor = QPalette().light().color()
        self.midlight: QColor = QPalette().midlight().color()
        self.dark: QColor = QPalette().dark().color()
        self.window: QColor = QPalette().window().color()
        self.text: QColor = QPalette().text().color()


class _Styles:
    _style_map: Dict[str, StyleParams] = {}
    _style_template: str

    def __init__(self):
        template = QFile(":/tt/StyleTemplate.qss")
        template.open(QFile.ReadOnly)
        self._style_template = bytes(template.readAll()).decode()

    def register_style(self, style_name: str, creator: StyleParams):
        if style_name not in self._style_map:
            self._style_map[style_name] = creator

    def unregister_style(self, style_name):
        if style_name in self._style_map:
            self._style_map.pop(style_name)

    def get_styletemplate(self):
        return self._style_template

    def is_registered(self, style_name: str) -> bool:
        return style_name in self._style_map

    def get_registered(self) -> List[str]:
        return list(self._style_map.keys())

    def get_style(self, style_name: str) -> Union[StyleParams, None]:
        if self.is_registered(style_name):
            return self._style_map[style_name]
        else:
            return None


_styles = _Styles()


def format_color(col: Union[QColor, List]) -> str:
    if isinstance(col, QColor) or isinstance(col, QtCore.Qt.GlobalColor):
        col = QColor(col)
        return "rgba({0}, {1}, {2}, {3})".format(
            col.red(), col.green(), col.blue(), col.alpha()
        )
    elif isinstance(col, Color):
        format_color(col.value)
    else:
        size = len(col)
        if size == 1:

            return format_color(col[0].value)
        result = "qlineargradient(x1:0, y1:1, x2:0, y2:0"
        for color in col:
            result += ", stop:{} {}".format(
                color.coefficient, format_color(color.value)
            )
        result += ")"
        return result


def get_styletemplate():
    return _styles.get_styletemplate()


def register_style(style_name: str, creator: StyleParams):
    return _styles.register_style(style_name, creator)


def unregister_style(style_name: str):
    _styles.unregister_style(style_name)


def is_registered(style_name: str) -> bool:
    return _styles.is_registered(style_name)


def get_styles() -> List[str]:
    return _styles.get_registered()


def get_defaultstyle() -> str:
    style = STYLE_COOL

    if platform == "win32":
        version_str = QSysInfo.kernelVersion()
        if "." in version_str:
            dot_index = version_str.index(".")
            if dot_index != -1:
                version_str = version_str[: dot_index + 2]
                version_str.replace(".", "0")
        version_double, ok = QLocale().toDouble(version_str)
        if version_double >= 602:
            style = STYLE_THRESHOLD
    elif platform == "darwin":
        style = STYLE_VIENNA

    return style


def fill_style(style: str, params: StyleParams) -> str:
    style = ""
    if params.UseTemplateSheet:
        style = get_styletemplate()
    style += params.AdditionalStyleSheet

    num_props = params.metaObject().propertyCount()
    for i in range(num_props):
        prop = params.metaObject().property(i)
        if prop.name() == "objectName":
            continue
        if prop.type() == QVariant.Bool:
            continue
        propstr = "%{0}%".format(prop.name())

        if propstr not in style:
            continue

        property = params.property(prop.name())
        if prop.type() is QVariant.String:
            style = style.replace(propstr, "{0}px".format(property))
        elif prop.type() is QVariant.Int or prop.type() == 2:
            style = style.replace(propstr, "{0}".format(property))
        elif prop.type() is QVariant.UserType:
            colors = property.value()
            style = style.replace(propstr, "{0}".format(format_color(colors)))
        elif prop.type() == 39:
            colors = property

            style = style.replace(propstr, "{0}".format(format_color(colors)))
    return style


def create_style(style_name: str) -> Union[StyleParams, None]:
    style = _styles.get_style(style_name)
    return style.copy()


def get_stylesheet(style: StyleParams) -> str:
    stylestr = fill_style("", style)
    return stylestr


def get_scalefactor(widget: QWidget) -> float:
    version = QT_VERSION_STR.split(".")
    screen: QScreen
    if int(version[0]) >= 5 and int(version[1]) >= 10:
        screen = QGuiApplication.screenAt(widget.mapToGlobal(QPoint(0, 0)))
    else:
        screen_nbr = QApplication.desktop().screenNumber(
            widget.mapToGlobal(QPoint(0, 0))
        )
        screens = QGuiApplication.screens()
        screen = screens[screen_nbr]

    factor = screen.logicalDotsPerInchY() / 96.0

    return factor


def get_pixelmetric(metric: QStyle.PixelMetric) -> int:
    if metric == QStyle.PM_SmallIconSize:
        return 16
    elif metric == QStyle.PM_LargeIconSize:
        return 32

    return QApplication.style().pixelMetrix(metric)


def _clampcolor(v: Union[int, float]) -> int:
    v = int(v)
    if v < 0:
        v = 0
    elif v > 255:
        v = 255
    return v


def _lcomb(
    c1: Union[QColor, QtCore.Qt.GlobalColor, Colors],
    c2: Union[QColor, QtCore.Qt.GlobalColor, Colors],
    f: float,
) -> QColor:
    fi = 1.0 - f
    if isinstance(c1, Colors):
        c1 = c1[0].value

    if isinstance(c2, Colors):
        c2 = c2[0].value
    c1 = QColor(c1)
    c2 = QColor(c2)

    return QColor(
        _clampcolor(c1.red() * f + c2.red() * fi),
        _clampcolor(c1.green() * f + c2.green() * fi),
        _clampcolor(c1.blue() * f + c2.blue() * fi),
        _clampcolor(c1.alpha() * f + c2.alpha() * fi),
    )


def _dimmed(c: QColor, factor: float) -> QColor:
    return _lcomb(c, QtCore.Qt.black, 1 - factor)


def _coeff(c: QColor, cr: float, cg: float, cb: float) -> QColor:
    return QColor(
        _clampcolor(c.red() * cr),
        _clampcolor(c.green() * cg),
        _clampcolor(c.blue() * cb),
    )


def _add(c1: QColor, c2: QColor) -> QColor:
    return QColor(
        _clampcolor(c1.red() + c2.red()),
        _clampcolor(c1.green() + c2.green()),
        _clampcolor(c1.blue() + c2.blue()),
        _clampcolor(c1.alpha() + c2.alpha()),
    )


def _basecolor(c: QColor) -> QColor:
    min_color = min(c.red(), c.green(), c.blue())
    return QColor(c.red() - min_color, c.green() - min_color, c.blue() - min_color)


def register_default_styles():
    palette: TPalette = TPalette()
    style_kool = StyleParams()
    style_kool.UseTemplateSheet = True
    style_kool.AdditionalStyleSheet = ""
    style_kool.TabBorderRadius = 0
    style_kool.TabFontColor = Colors(palette.text)
    style_kool.ToolbarBackgroundColor = Colors(palette.window)
    style_kool.BorderColor = Colors(_dimmed(palette.light, 0.25))
    style_kool.GroupNameColor = Colors(_lcomb(palette.text, palette.midlight, 0.4))
    style_kool.TabSpecialColor = Colors(
        [
            Color(0.0, _dimmed(palette.highlight, 0.2)),
            Color(1.0, palette.highlight),
        ]
    )
    style_kool.TabSpecialHoverColor = Colors(
        [
            Color(0.0, style_kool.TabSpecialColor[1].value),
            Color(1.0, style_kool.TabSpecialColor[0].value),
        ]
    )
    style_kool.TabSpecialHoverBorderColor = Colors(palette.highlight)
    style_kool.TabSpecialHoverBorderColorSide = Colors(
        style_kool.TabSpecialHoverBorderColor()
    )
    style_kool.TabSpecialBorderColor = Colors(palette.highlight)
    style_kool.TabSpecialBorderColorSide = Colors(style_kool.TabSpecialBorderColor())
    style_kool.TabSpecialFontColor = Colors(palette.htext)
    style_kool.TabUnselectedHoverBorderColorTop = Colors(palette.highlight)
    style_kool.TabHoverBorderColorTop = Colors(palette.highlight)
    style_kool.TabUnselectedHoverBorderColorSide = Colors(
        [
            Color(0.0, style_kool.BorderColor()),
            Color(0.1, style_kool.BorderColor()),
            Color(0.7, style_kool.TabHoverBorderColorTop()),
            Color(1.0, style_kool.TabHoverBorderColorTop()),
        ]
    )
    style_kool.TabHoverBorderColorSide = Colors(
        [
            Color(0.0, style_kool.BorderColor()),
            Color(0.1, style_kool.BorderColor()),
            Color(0.7, style_kool.TabHoverBorderColorTop()),
            Color(1.0, style_kool.TabHoverBorderColorTop()),
        ]
    )
    style_kool.PaneColor = Colors(
        [
            Color(0.0, _dimmed(palette.light, 0.1)),
            Color(0.7, palette.light),
            Color(1.0, palette.light),
        ]
    )
    style_kool.TabSelectedColor = Colors(palette.light)
    style_kool.TabUnselectedColor = Colors(
        _lcomb(
            style_kool.ToolbarBackgroundColor, style_kool.TabSelectedColor[0].value, 0.5
        )
    )
    style_kool.SeparatorColor = Colors(
        [
            Color(0.0, QColor(QtCore.Qt.transparent)),
            Color(0.05, QColor(QtCore.Qt.transparent)),
            Color(0.1, style_kool.BorderColor()),
            Color(0.9, style_kool.BorderColor()),
            Color(0.95, QColor(QtCore.Qt.transparent)),
            Color(1.0, QColor(QtCore.Qt.transparent)),
        ]
    )
    style_kool.HorizontalFrameBackgroundColor = Colors(style_kool.PaneColor())
    for c in style_kool.HorizontalFrameBackgroundColor:
        c.value.setAlpha(100)
    style_kool.HorizontalFrameBorderColor = Colors(style_kool.BorderColor())
    style_kool.HorizontalFrameBorderSize = 2
    style_kool.TabSpacing = 3
    style_kool.HideArrowColor = Colors(_lcomb(palette.text, palette.midlight, 0.4))

    vienna = (
        QColor(51, 153, 255)
        if palette.window.lightnessF() > 0.5
        else QColor(25, 40, 70)
    )
    style_vienna = StyleParams()
    style_vienna.UseTemplateSheet = True
    style_vienna.AdditionalStyleSheet = ""
    style_vienna.TabBorderRadius = 2
    style_vienna.TabFontColor = Colors(_lcomb(palette.text, vienna, 0.588))
    style_vienna.ToolbarBackgroundColor = Colors(
        _add(_dimmed(palette.window, 0.07), _basecolor(_dimmed(vienna, 0.892)))
    )
    dim_coeff = 0.225 if palette.window.lightnessF() > 0.5 else 0.5
    style_vienna.BorderColor = Colors(
        _add(_dimmed(palette.window, dim_coeff), _basecolor(_dimmed(vienna, 0.838)))
    )
    style_vienna.GroupNameColor = Colors(
        _lcomb(palette.text, style_vienna.ToolbarBackgroundColor, 0.484)
    )

    style_vienna.PaneColor = Colors(
        [
            Color(0.0, style_vienna.ToolbarBackgroundColor),
            Color(0.5, style_vienna.ToolbarBackgroundColor),
            Color(
                0.75, _lcomb(style_vienna.ToolbarBackgroundColor, palette.light, 0.5)
            ),
            Color(1.0, palette.light),
        ]
    )

    style_vienna.TabSpecialColor = Colors(
        [
            Color(
                0.0,
                _add(
                    _dimmed(palette.window, 0.7125),
                    _coeff(
                        _basecolor(_dimmed(palette.highlight, 0.294)), 1.0, 1.29, 1.0
                    ),
                ),
            ),
            Color(
                0.6,
                _add(
                    _dimmed(palette.window, 0.891),
                    _coeff(
                        _basecolor(_dimmed(palette.highlight, 0.46)), 1.0, 0.69, 1.0
                    ),
                ),
            ),
            Color(
                0.6001,
                _add(
                    _dimmed(palette.window, 0.825),
                    _coeff(
                        _basecolor(_dimmed(palette.highlight, 0.362)), 1.0, 0.815, 1.0
                    ),
                ),
            ),
            Color(
                1.0,
                _add(
                    _dimmed(palette.window, 0.7125),
                    _coeff(
                        _basecolor(_dimmed(palette.highlight, 0.416)), 1.0, 0.924, 1.0
                    ),
                ),
            ),
        ]
    )

    style_vienna.TabSpecialHoverColor = Colors(
        [
            Color(
                0.0, _coeff(style_vienna.TabSpecialColor[0].value, 2.17, 1.48, 1.197)
            ),
            Color(
                0.6, _coeff(style_vienna.TabSpecialColor[1].value, 0.653, 1.218, 1.286)
            ),
            Color(
                0.6001,
                _coeff(style_vienna.TabSpecialColor[2].value, 1.69, 1.326, 1.191),
            ),
            Color(
                1.0, _coeff(style_vienna.TabSpecialColor[3].value, 1.768, 1.44, 1.255)
            ),
        ]
    )

    style_vienna.TabSpecialHoverBorderColor = Colors(
        _add(
            _dimmed(palette.window, 0.729),
            _coeff(_basecolor(_dimmed(palette.highlight, 0.392)), 1.0, 0.66, 1.0),
        )
    )
    style_vienna.TabSpecialBorderColor = Colors(
        _add(
            _dimmed(palette.window, 0.729),
            _coeff(_basecolor(_dimmed(palette.highlight, 0.392)), 1.0, 0.66, 1.0),
        )
    )
    style_vienna.TabSpecialHoverBorderColorSide = Colors(
        style_vienna.TabSpecialBorderColor()
    )
    style_vienna.TabSpecialBorderColorSide = Colors(
        style_vienna.TabSpecialBorderColor()
    )
    style_vienna.TabSpecialFontColor = Colors(palette.htext)
    style_vienna.TabUnselectedHoverBorderColorTop = Colors(QColor(255, 183, 0))
    style_vienna.TabHoverBorderColorTop = Colors(QColor(255, 183, 0))

    style_vienna.TabUnselectedHoverBorderColorSide = Colors(
        [
            Color(0.0, style_vienna.BorderColor()),
            Color(0.3, QColor(255, 183, 0)),
            Color(1.0, QColor(255, 183, 0)),
        ]
    )
    style_vienna.TabHoverBorderColorSide = Colors(
        style_vienna.TabUnselectedHoverBorderColorSide()
    )

    style_vienna.TabUnselectedColor = Colors(
        _add(_dimmed(palette.window, 0.02), _basecolor(_dimmed(vienna, 0.9264)))
    )

    style_vienna.TabSelectedColor = Colors(palette.light)

    style_vienna.SeparatorColor = Colors(
        [
            Color(0.0, QtCore.Qt.transparent),
            Color(0.075, QtCore.Qt.transparent),
            Color(
                0.0751,
                _add(
                    _dimmed(palette.window, 0.3125), _basecolor(_dimmed(vienna, 0.789))
                ),
            ),
            Color(
                0.925,
                _add(
                    _dimmed(palette.window, 0.3125), _basecolor(_dimmed(vienna, 0.789))
                ),
            ),
            Color(0.9251, QtCore.Qt.transparent),
            Color(1.0, QtCore.Qt.transparent),
        ]
    )

    style_vienna.HorizontalFrameBackgroundColor = Colors(
        [
            Color(
                0.0,
                _add(
                    _dimmed(palette.window, 0.033),
                    _coeff(_basecolor(_dimmed(vienna, 0.9362)), 1.0, 1.38, 1.0),
                ),
            ),
            Color(
                0.6,
                _add(
                    _dimmed(palette.window, 0.05),
                    _coeff(_basecolor(_dimmed(vienna, 0.8333)), 1.0, 0.588, 1.0),
                ),
            ),
            Color(
                0.6001,
                _add(
                    palette.window,
                    _coeff(_basecolor(_dimmed(vienna, 0.9166)), 1.0, 0.82, 1.0),
                ),
            ),
            Color(1.0, palette.light),
        ]
    )

    style_vienna.HorizontalFrameBorderColor = Colors(style_vienna.BorderColor())
    style_vienna.HorizontalFrameBorderSize = 2
    style_vienna.TabSpacing = 4
    style_vienna.HideArrowColor = Colors(_lcomb(palette.text, palette.light, 0.62))

    style_threshold = StyleParams()
    style_threshold.UseTemplateSheet = True
    style_threshold.AdditionalStyleSheet = ""
    style_threshold.TabBorderRadius = 0
    style_threshold.TabFontColor = Colors(palette.text)
    style_threshold.ToolbarBackgroundColor = Colors(palette.light)
    pane_dimmcoeff = 0.03529 if palette.window.lightnessF() > 0.5 else 0.1
    style_threshold.PaneColor = Colors(_dimmed(palette.light, pane_dimmcoeff))
    border_dimmcoeff = 0.15 if palette.window.lightnessF() > 0.5 else 0.3
    style_threshold.BorderColor = Colors(
        _dimmed(style_threshold.ToolbarBackgroundColor, border_dimmcoeff)
    )
    style_threshold.GroupNameColor = Colors(_lcomb(palette.text, palette.light, 0.43))

    style_threshold.TabSpecialColor = Colors(_coeff(palette.highlight, 0.5, 0.8, 0.8))
    style_threshold.TabSpecialHoverColor = Colors(
        _coeff(palette.highlight, 0.8, 0.9, 0.88)
    )
    style_threshold.TabSpecialHoverBorderColor = Colors(
        style_threshold.TabSpecialColor()
    )
    style_threshold.TabSpecialBorderColor = Colors(style_threshold.TabSpecialColor())
    style_threshold.TabSpecialHoverBorderColorSide = Colors(
        style_threshold.TabSpecialColor()
    )
    style_threshold.TabSpecialBorderColorSide = Colors(
        style_threshold.TabSpecialColor()
    )
    style_threshold.TabSpecialFontColor = Colors(palette.htext)

    style_threshold.TabUnselectedHoverBorderColorTop = Colors(
        _dimmed(style_threshold.PaneColor, 0.04)
    )
    style_threshold.TabHoverBorderColorTop = Colors(style_threshold.BorderColor())
    style_threshold.TabUnselectedHoverBorderColorSide = Colors(
        style_threshold.TabUnselectedHoverBorderColorTop()
    )

    style_threshold.TabHoverBorderColorSide = Colors(style_threshold.BorderColor())

    unselected_dimmcoeff = 0.008 if palette.window.lightnessF() > 0.5 else 0.1
    style_threshold.TabUnselectedColor = Colors(
        _dimmed(style_threshold.ToolbarBackgroundColor, unselected_dimmcoeff)
    )

    style_threshold.TabSelectedColor = Colors(style_threshold.PaneColor())

    style_threshold.SeparatorColor = Colors(
        [
            Color(0.0, QtCore.Qt.transparent),
            Color(0.05, QtCore.Qt.transparent),
            Color(0.051, style_threshold.BorderColor()),
            Color(0.95, style_threshold.BorderColor()),
            Color(0.951, QtCore.Qt.transparent),
            Color(1.0, QtCore.Qt.transparent),
        ]
    )

    style_threshold.HorizontalFrameBackgroundColor = Colors(QtCore.Qt.transparent)

    style_threshold.HorizontalFrameBorderColor = Colors(QtCore.Qt.transparent)
    style_threshold.HorizontalFrameBorderSize = 0
    style_threshold.TabSpacing = 2

    style_threshold.HideArrowColor = Colors(_lcomb(palette.text, palette.light, 0.62))

    register_style(STYLE_COOL, style_kool)
    register_style(STYLE_VIENNA, style_vienna)
    register_style(STYLE_THRESHOLD, style_threshold)

    style_whitemercy: StyleParams = create_style(STYLE_THRESHOLD)
    style_whitemercy.TabUnselectedColor = Colors(style_whitemercy.PaneColor())
    style_whitemercy.PaneColor = Colors(style_whitemercy.ToolbarBackgroundColor())
    style_whitemercy.TabSelectedColor = Colors(style_whitemercy.PaneColor())
    style_whitemercy.BorderColor = Colors(_dimmed(style_whitemercy.BorderColor(), 0.1))
    style_whitemercy.TabHoverBorderColorTop = Colors(style_whitemercy.BorderColor())
    style_whitemercy.TabHoverBorderColorSide = Colors(style_whitemercy.BorderColor())
    style_whitemercy.SeparatorColor = Colors(
        [
            Color(0.0, QtCore.Qt.transparent),
            Color(0.05, QtCore.Qt.transparent),
            Color(0.051, style_whitemercy.BorderColor()),
            Color(0.95, style_whitemercy.BorderColor()),
            Color(0.951, QtCore.Qt.transparent),
            Color(1.0, QtCore.Qt.transparent),
        ]
    )

    register_style(STYLE_WHITEMERCY, style_whitemercy)
