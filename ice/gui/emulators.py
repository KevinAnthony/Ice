"""
emulators.py

Created by Scott on 2016-03-08.
Copyright (c) 2016 Kevin Anthony. All rights reserved.
"""

from copy import copy

from ice.gui import config

from PyQt5 import QtGui, QtWidgets, QtCore

class EmulatoreGui(config.Config):

    def __init__(self, parent = None, settings = None):
        super(EmulatoreGui, self).__init__(parent)
        self.app_settings = settings

        self.consoles = copy(settings.consoles)
        self.emulators = copy(settings.emulators)

        self.app_settings = settings

        first_emulator = None
        for emulator in self.emulators:
            if first_emulator is None:
                first_emulator = emulator
            action = self.create_emulator(emulator)
            self.toolbar.addAction(action)
            self.toolbar.adjustSize()

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

        self.on_edit_emulator(first_emulator)

    def create_emulator(self, emulator):
        if emulator is None:
            return
        icon = self.icon_from_exec(emulator.location)
        if icon is None or icon.isNull():
            icon = QtGui.QIcon("../icon.ico")
        return self.create_action(icon, emulator.name, lambda: self.on_edit_emulator(emulator))

    def on_edit_emulator(self, emulator):
        self.emulator_label.setText(emulator.name)

