from PyQt5 import QtGui, QtWidgets, QtCore


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
