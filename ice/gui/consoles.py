"""
consoles.py

Created by Scott on 2016-03-08.
Copyright (c) 2016 Kevin Anthony. All rights reserved.
"""

from PyQt5 import QtGui, QtWidgets, QtCore

from copy import copy


class ConsoleGui(QtWidgets.QDialog):
    def __init__(self, parent=None, settings=None):
        super(ConsoleGui, self).__init__(parent)

        self.consoles = copy(settings.consoles)
        self.emulators = copy(settings.emulators)

        self.app_settings = settings
        self.setFixedSize(800, 600)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.accepted.connect(self.on_ok)
        self.buttonBox.rejected.connect(self.on_cancel)

        main = QtWidgets.QWidget(self)
        self.workspace_widget = QtWidgets.QWidget(self)
        self.workspace_widget.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))
        self.workspace = QtWidgets.QVBoxLayout(self.workspace_widget)

        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.addWidget(main)
        self.verticalLayout.addWidget(self.buttonBox)

        horizontal_layout = QtWidgets.QHBoxLayout(main)

        toolbar = QtWidgets.QToolBar()
        toolbar.setIconSize(QtCore.QSize(50, 50))
        toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        toolbar.setMovable(False)
        toolbar.setFloatable(False)
        toolbar.setOrientation(QtCore.Qt.Vertical)
        toolbar.setStyleSheet("QToolBar { border: 0px; background: #fff;}")

        first_console = None
        for console in self.consoles:
            if first_console is None:
                first_console = console
            self.create_console(console, toolbar)

        #Set all Workspace widgets up here
        self.emulator_label = QtWidgets.QLabel("")
        self.emulator_label.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        old_font = self.emulator_label.font()
        font = old_font.family()
        self.emulator_label.setFont(QtGui.QFont(font, 24))
        self.emulator_label.setContentsMargins(0, 0, 0, 0)
        self.emulator_label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.workspace.addWidget(self.emulator_label)

        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.workspace.addWidget(line)

        self.shortname = QtWidgets.QLineEdit()
        self.create_config_line("Nickname", self.shortname)

        self.extensions = QtWidgets.QLineEdit()
        self.create_config_line("Extensions", self.extensions)

        self.custom_roms_directory = QtWidgets.QLineEdit()
        self.create_config_line("Custom Rom Directory", self.custom_roms_directory)

        self.prefix = QtWidgets.QLineEdit()
        self.create_config_line("Prefix", self.prefix)

        self.icon = QtWidgets.QLineEdit()
        self.create_config_line("Icon", self.icon)

        self.images_directory = QtWidgets.QLineEdit()
        self.create_config_line("Extensions", self.images_directory)

        self.emulator_combobox = QtWidgets.QComboBox()
        self.create_config_line("Default Emulator", self.emulator_combobox)

        # END **Set all Workspace widgets up here**
        self.workspace.setAlignment(QtCore.Qt.AlignTop )

        scroll = QtWidgets.QScrollArea()
        scroll.setWidget(toolbar)
        scroll.setStyleSheet("QScrollArea {background: #fff;}")
        scroll.setAlignment(QtCore.Qt.AlignCenter)
        scroll.setMaximumWidth(175)
        horizontal_layout.addWidget(scroll)
        horizontal_layout.addWidget(self.workspace_widget)

        self.on_edit_console(first_console)

    def on_ok(self):
        # TODO write to app_settings
        # self.app_settings.consoles = copy(self.consoles)
        # TODO write to consoles.txt
        self.close()

    def on_cancel(self):
        self.close()

    def create_console(self, console, toolbar):
        if console is None:
            return
        icon = QtGui.QIcon(console.icon)
        if icon is None or icon.isNull():
            icon = QtWidgets.QIcon("../icon.ico")
        self.create_action(icon, console.shortname, toolbar, lambda: self.on_edit_console(console) )

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

    def create_action(self, icon, text, parent, click):
        action = QtWidgets.QAction(self)
        action.setIcon(icon)
        action.setText(text)
        parent.addAction(action)
        action.triggered.connect(click)

    def find_console(self, name):
        for c in self.consoles:
            if c.fullname == name:
                return c
        return None

    def on_edit_console(self, console):
        if console is None:
            return
        icon = console.icon
        self.emulator_label.setText(console.fullname)
        self.shortname.setText(console.shortname)
        self.extensions.setText(console.extensions)
        self.custom_roms_directory.setText(console.custom_roms_directory)
        self.prefix.setText(console.prefix)
        self.icon.setText(console.icon)
        self.images_directory.setText(console.images_directory)
        self.emulator_combobox.clear()
        for emulator in self.emulators:
            self.emulator_combobox.addItem(emulator.name)
        index = self.emulator_combobox.findText(console.emulator.name, QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.emulator_combobox.setCurrentIndex(index)



