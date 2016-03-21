"""
emulators.py

Created by Scott on 2016-03-08.
Copyright (c) 2016 Kevin Anthony. All rights reserved.
"""
from PyQt5 import Qt, QtWidgets, QtCore

class EmulatoreGui(QtWidgets.QDialog):
  def __init__(self, parent = None, settings = None):
    super(EmulatoreGui, self).__init__(parent)
    self.app_settings = settings
    self.buttonBox = QtWidgets.QDialogButtonBox(self)
    self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
    self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)

    self.textBrowser = QtWidgets.QTextBrowser(self)
    self.textBrowser.append("This is a QTextBrowser!")

    self.verticalLayout = QtWidgets.QVBoxLayout(self)
    self.verticalLayout.addWidget(self.textBrowser)
    self.verticalLayout.addWidget(self.buttonBox)
