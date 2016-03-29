"""
consoles.py

Created by Scott on 2016-03-08.
Copyright (c) 2016 Kevin Anthony. All rights reserved.
"""

from copy import copy

from ice.gui import config

from PyQt5 import QtGui, QtWidgets, QtCore

class ConsoleGui(config.Config):

    def __init__(self, parent=None, settings=None):
        super(ConsoleGui, self).__init__(parent)

        self.consoles = copy(settings.consoles)
        self.emulators = copy(settings.emulators)

        self.app_settings = settings

        first_console = None
        for console in self.consoles:
            if first_console is None:
                first_console = console
            action = self.create_console(console)
            self.toolbar.addAction(action)
        self.toolbar.adjustSize()

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
        self.refresh_size()
        self.on_edit_console(first_console)

    def create_console(self, console):
        if console is None:
            return
        icon = QtGui.QIcon(console.icon)
        if icon is None or icon.isNull():
            icon = QtWidgets.QIcon("../icon.ico")
        return self.create_action(icon, console.shortname, lambda: self.on_edit_console(console) )

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

    def on_ok(self):
        # TODO write to app_settings
        # TODO write to consoles.txt
        self.close()