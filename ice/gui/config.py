from PyQt5 import QtGui, QtWidgets, QtCore
import os, platform
if os.name == "nt":
    import win32ui
    import win32gui
    import win32api
    import win32con
    from PyQt5.QtWinExtras import QtWin


class Config(QtWidgets.QDialog):
    def __init__(self, parent):
        super(Config, self).__init__(parent)
        self.setFixedSize(800, 600)

        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Save)
        add_button = self.buttonBox.addButton("Add", QtWidgets.QDialogButtonBox.ResetRole)
        rem_button = self.buttonBox.addButton("Remove", QtWidgets.QDialogButtonBox.ResetRole)
        self.buttonBox.accepted.connect(self.on_ok)
        self.buttonBox.rejected.connect(self.on_cancel)
        add_button.clicked.connect(self.on_add)
        rem_button.clicked.connect(self.on_remove)

        main = QtWidgets.QWidget(self)

        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.addWidget(main)
        self.verticalLayout.addWidget(self.buttonBox)

        horizontal_layout = QtWidgets.QHBoxLayout(main)

        self.workspace_widget = QtWidgets.QWidget(self)
        self.workspace_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.workspace = QtWidgets.QVBoxLayout(self.workspace_widget)

        self.workspace.setAlignment(QtCore.Qt.AlignTop )

        self.toolbar = QtWidgets.QToolBar()
        self.toolbar.setIconSize(QtCore.QSize(50, 50))
        self.toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolbar.setMovable(False)
        self.toolbar.setFloatable(False)
        self.toolbar.setOrientation(QtCore.Qt.Vertical)
        self.toolbar.setStyleSheet("QToolBar { border: 0px; background: #fff;}")
        self.toolbar.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)

        self.toolbar_scroll = QtWidgets.QScrollArea()
        self.toolbar_scroll.setWidget(self.toolbar)
        self.toolbar_scroll.setStyleSheet("QScrollArea {background: #fff;}")
        self.toolbar_scroll.setAlignment(QtCore.Qt.AlignCenter)
        self.toolbar_scroll.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.toolbar_scroll.setMinimumWidth(100)

        horizontal_layout.addWidget(self.toolbar_scroll)
        horizontal_layout.addWidget(self.workspace_widget)

    def refresh_size(self):
        self.toolbar.adjustSize()
        self.toolbar_scroll.adjustSize()

    def create_action(self, icon, text, click):
        action = QtWidgets.QAction(icon, text, self)
        action.triggered.connect(click)
        return action

    def create_config_line(self, label_text, settings_widget):
        widget = QtWidgets.QWidget()
        self.workspace.addWidget(widget)

        hbox = QtWidgets.QHBoxLayout(widget)

        label = QtWidgets.QLabel(label_text)
        label.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        hbox.addWidget(label)

        if not type(settings_widget) is QtWidgets.QComboBox:
            settings_widget.setAlignment(QtCore.Qt.AlignTop)
        settings_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        hbox.addWidget(settings_widget)

    def on_ok(self):
        self.close()

    def on_cancel(self):
        self.close()

    def on_add(self):
        pass

    def on_remove(self):
        pass

    def icon_from_exec(self, path):
        if (os.name == "nt"):
            return self.icon_from_exec_win(path)
        if (os.name == "posix"):
            if (platform.system() == "Darwin"):
                return self.icon_from_exec_mac(path)
            if (platform.system() == "Linux"):
                return self.icon_from_exec_nix(path)
        return None

    def icon_from_exec_mac(self, path):
        return None

    def icon_from_exec_nix(self, path):
        return None

    def icon_from_exec_win(self, path):
        large, small = win32gui.ExtractIconEx(path, 0)
        for i in small:
            win32gui.DestroyIcon(i)
        pixmap = QtWin.fromHBITMAP(self.bitmapFromHIcon(large[0]),1)
        for i in large:
            win32gui.DestroyIcon(i)
        return QtGui.QIcon(pixmap)

    def bitmapFromHIcon(self, hIcon):
        hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
        hbmp = win32ui.CreateBitmap()
        hbmp.CreateCompatibleBitmap(hdc, 32, 32)
        hdc = hdc.CreateCompatibleDC()
        hdc.SelectObject(hbmp)
        hdc.DrawIcon((0, 0), hIcon)
        hdc.DeleteDC()
        return hbmp.GetHandle()