"""
consoles.py

Created by Scott on 2016-03-08.
Copyright (c) 2016 Kevin Anthony. All rights reserved.
"""

from PyQt4 import QtGui, QtCore

from copy import copy


class ConsoleGui(QtGui.QDialog):
    def __init__(self, parent=None, settings=None):
        super(ConsoleGui, self).__init__(parent)

        self.consoles = copy(settings.consoles)

        self.app_settings = settings
        self.setFixedSize(800, 600)
        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok)
        self.buttonBox.accepted.connect(self.on_ok)
        self.buttonBox.rejected.connect(self.on_cancel)

        main = QtGui.QWidget(self)
        self.workspace = QtGui.QWidget(self)
        self.workspace.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding))

        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.verticalLayout.addWidget(main)
        self.verticalLayout.addWidget(self.buttonBox)

        horizontal_layout = QtGui.QHBoxLayout(main)

        toolbar = QtGui.QToolBar()
        toolbar.setIconSize(QtCore.QSize(50, 50))
        toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        toolbar.setMovable(False)
        toolbar.setFloatable(False)
        toolbar.setOrientation(QtCore.Qt.Vertical)
        toolbar.setStyleSheet("QToolBar { border: 0px; background: #fff;}")

        for console in self.consoles:
            self.create_console(console, toolbar)
        #self.create_console("Nintendo Entertainment System", toolbar, self.on_nes)
        #self.create_console("Super Nintendo", toolbar, self.on_snes)
        #self.create_console("Nintendo 64", toolbar, self.on_n64)
        #self.create_console("Nintendo Gamecube", toolbar, self.on_gc)
        #self.create_console("Nintendo Wii", toolbar, self.on_wii)
        #self.create_console("Nintendo Gameboy", toolbar, self.on_gb)
        #self.create_console("Gameboy Advance", toolbar, self.on_gba)
        #self.create_console("Nintendo DS", toolbar, self.on_ds)
        #self.create_console("Playstation 1", toolbar, self.on_ps1)
        #self.create_console("Playstation 2", toolbar, self.on_ps2)
        #self.create_console("Sega Genesis", toolbar, self.on_genesis)
        #self.create_console("Sega Dreamcast", toolbar, self.on_dreamcast)

        self.emulator_label = QtGui.QLabel("", self.workspace)
        self.emulator_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignHCenter)
        old_font = self.emulator_label.font()
        new_font = QtGui.QFont(old_font.family(), 24)
        self.emulator_label.setFont(new_font)
        self.emulator_label.setContentsMargins(0, 0, 0, 0)
        self.emulator_label.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)

        line = QtGui.QFrame(self.workspace)
        line.setFrameShape(QtGui.QFrame.HLine)
        line.setFrameShadow(QtGui.QFrame.Sunken)

        scroll = QtGui.QScrollArea()
        scroll.setWidget(toolbar)
        scroll.setStyleSheet("QScrollArea {background: #fff;}")
        scroll.setAlignment(QtCore.Qt.AlignCenter)
        scroll.setMaximumWidth(175)
        horizontal_layout.addWidget(scroll)
        horizontal_layout.addWidget(self.workspace)

    def on_ok(self):
        # TODO write to app_settings
        # self.app_settings.consoles = copy(self.consoles)
        # TODO write to consoles.txt
        self.close()

    def on_cancel(self):
        self.close()

    def create_console(self, console, toolbar):
        #console = self.find_console(name)
        if console is None:
            return
        icon = QtGui.QIcon(console.icon)
        if icon is None or icon.isNull():
            icon = QtGui.QIcon("../icon.ico")
        self.create_action(icon, console.shortname, toolbar, lambda: self.on_edit_console(console) )

    def create_action(self, icon, text, parent, click):
        action = QtGui.QAction(self)
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
        icon = console.icon
        self.emulator_label.setText(console.fullname)
        self.emulator_label.setMinimumWidth(self.workspace.width())
