from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QCheckBox,
    QLabel,
    QMainWindow,
    QPushButton,
    QTextEdit,
)
from mainwindow import Ui_MainWindow
import sys

sys.path.append("../../src")
from pytabtoolbar import (
    Builder,
    get_styles,
    register_style,
    StyleParams,
    get_defaultstyle,
)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.statusBar.addPermanentWidget(QLabel("Some fancy status."))
        builder = Builder(self)
        builder.set_widgetcreator("textEdit", QTextEdit)
        builder.set_widgetcreator("checkBox", QCheckBox)
        builder.set_widgetcreator("pushButton", QPushButton)

        tabtoolbar = builder.create_tabtoolbar("://tt/tabtoolbar.json")
        self.addToolBar(QtCore.Qt.TopToolBarArea, tabtoolbar)

        widget = builder["customTextEdit"]
        widget.setMaximumWidth(100)

        widget = builder["customCheckBox"]
        widget.setText("Check 1")

        btn = builder["customEditButton"]
        btn.setText("Edit")

        self.kek = True
        self.edit_page = builder["Edit"]
        btn.clicked.connect(self.show_editpage)

        styles_group = builder["Styles"]
        styles_group.add_separator()
        styles = get_styles()
        for style in styles:
            btn = QPushButton(style, self)
            btn.clicked.connect(lambda state, x=style: tabtoolbar.set_style(x))
            styles_group.add_widget(btn)

        params = StyleParams()
        params.UseTemplateSheet = False
        params.AdditionalStyleSheet = ""
        register_style("NoStyle", params)

        btn_nativestyle = builder["nativeStyleButton"]
        btn_nativestyle.setText("No Style")
        btn_nativestyle.clicked.connect(lambda state: tabtoolbar.set_style("NoStyle"))

        btn_defaultstyle = builder["defaultStyleButton"]
        btn_defaultstyle.setText("Default")
        btn_defaultstyle.clicked.connect(
            lambda state: tabtoolbar.set_style(get_defaultstyle())
        )

    @QtCore.pyqtSlot()
    def show_editpage(self):
        if self.kek:
            self.edit_page.hide()
        else:
            self.edit_page.show()
        self.kek = not self.kek


if __name__ == "__main__":
    # QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    app = QtWidgets.QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())
