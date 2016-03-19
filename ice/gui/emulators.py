"""
emulators.py

Created by Scott on 2016-03-08.
Copyright (c) 2016 Kevin Anthony. All rights reserved.
"""
from PyQt4 import Qt, QtGui, QtCore

class EmulatoreGui(QtGui.QDialog):
  def __init__(self, parent = None, settings = None):
    super(EmulatoreGui, self).__init__(parent)
    self.app_settings = settings
    self.buttonBox = QtGui.QDialogButtonBox(self)
    self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
    self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)

    self.textBrowser = QtGui.QTextBrowser(self)
    self.textBrowser.append("This is a QTextBrowser!")

    self.verticalLayout = QtGui.QVBoxLayout(self)
    self.verticalLayout.addWidget(self.textBrowser)
    self.verticalLayout.addWidget(self.buttonBox)