"""
consoles.py

Created by Scott on 2016-03-08.
Copyright (c) 2016 Kevin Anthony. All rights reserved.
"""
from PyQt4 import Qt, QtGui, QtCore

class ConsoleGui(QtGui.QDialog):
  def __init__(self, parent = None):
    super(ConsoleGui, self).__init__(parent)

    self.setFixedSize(800,600)
    self.buttonBox = QtGui.QDialogButtonBox(self)
    self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
    self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)

    main = QtGui.QWidget(self)
    work = QtGui.QWidget(self)
    work.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding))

    self.verticalLayout = QtGui.QVBoxLayout(self)
    self.verticalLayout.addWidget(main)
    self.verticalLayout.addWidget(self.buttonBox)

    horizontalLayout = QtGui.QHBoxLayout(main)

    toolbar = QtGui.QToolBar()
    toolbar.setIconSize(QtCore.QSize(50,50))
    toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
    toolbar.setMovable(False)
    toolbar.setFloatable(False)
    toolbar.setOrientation(QtCore.Qt.Vertical)
    toolbar.setStyleSheet("QToolBar { border: 0px; background: #fff;}")

    self.create_action(QtGui.QIcon("../icon.ico"), "NES", toolbar, self.on_nes)
    self.create_action(QtGui.QIcon("../icon.ico"), "SNES", toolbar, self.on_snes)
    self.create_action(QtGui.QIcon("../icon.ico"), "N64", toolbar, self.on_n64)
    self.create_action(QtGui.QIcon("../icon.ico"), "GameCube", toolbar, self.on_gc)
    self.create_action(QtGui.QIcon("../icon.ico"), "Wii", toolbar, self.on_wii)
    self.create_action(QtGui.QIcon("../icon.ico"), "GameBoy", toolbar, self.on_gb)
    self.create_action(QtGui.QIcon("../icon.ico"), "GameBoy Advanced", toolbar, self.on_gba)
    self.create_action(QtGui.QIcon("../icon.ico"), "GameBoy DS", toolbar, self.on_ds)
    self.create_action(QtGui.QIcon("../icon.ico"), "PlayStation 1", toolbar, self.on_ps1)
    self.create_action(QtGui.QIcon("../icon.ico"), "PlayStation 2", toolbar, self.on_ps2)
    self.create_action(QtGui.QIcon("../icon.ico"), "Sega Genesis", toolbar, self.on_genesis)
    self.create_action(QtGui.QIcon("../icon.ico"), "Sega Dreamcast", toolbar, self.on_dreamcast)

    scroll = QtGui.QScrollArea()
    scroll.setWidget(toolbar)
    scroll.setStyleSheet("QScrollArea {background: #fff;}")
    scroll.setAlignment(QtCore.Qt.AlignCenter)
    scroll.setMaximumWidth(175)
    horizontalLayout.addWidget(scroll)
    horizontalLayout.addWidget(work)

  def create_action(self, icon, text, parent, click):
    action = QtGui.QAction(self)
    action.setIcon(icon)
    action.setText(text)
    parent.addAction(action)
    action.triggered.connect(click)

  def on_nes(self):
    name = "Nintendo Entertainment System"
    self.on_edit_console(name)

  def on_snes(self):
    name = "Super Nintendo"
    self.on_edit_console(name)

  def on_n64(self):
    name = "Nintendo 64"
    self.on_edit_console(name)

  def on_gc(self):
    name = "Nintendo Gamecube"
    self.on_edit_console(name)

  def on_wii(self):
    name = "Nintendo Wii"
    self.on_edit_console(name)

  def on_ps1(self):
    name = "Playstation 1"
    self.on_edit_console(name)

  def on_ps2(self):
    name = "Playstation 2"
    self.on_edit_console(name)

  def on_genesis(self):
    name = "Sega Genesis"
    self.on_edit_console(name)

  def on_dreamcast(self):
    name = "Sega Dreamcast"
    self.on_edit_console(name)

  def on_gb(self):
    name = "Nintendo Gameboy"
    self.on_edit_console(name)

  def on_gba(self):
    name = "Gameboy Advance"
    self.on_edit_console(name)

  def on_ds(self):
    name = "Nintendo DS"
    self.on_edit_console(name)

  def on_edit_console(self, name):
    pass