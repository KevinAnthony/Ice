"""
consoles.py

Created by Scott on 2016-03-08.
Copyright (c) 2016 Kevin Anthony. All rights reserved.
"""

from PyQt5 import QtGui, QtWidgets, QtCore

from ice.gui import config

from copy import copy


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
        self.console_label = QtWidgets.QLabel("")
        self.console_label.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        old_font = self.console_label.font()
        font = old_font.family()
        self.console_label.setFont(QtGui.QFont(font, 24))
        self.console_label.setContentsMargins(0, 0, 0, 0)
        self.console_label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.workspace.addWidget(self.console_label)

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

    def on_ok(self):
        self.saveConsoleSettings()
        self.close()

    def create_console(self, console):
        if console is None:
            return
        icon = QtGui.QIcon(console.icon)
        if icon is None or icon.isNull():
            icon = QtGui.QIcon("../icon.ico")
        return self.create_action(icon, console.shortname, lambda: self.on_edit_console(console) )

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

    def saveConsoleSettings(self):
        temp_file = "../consoles.txt"
        f = open(temp_file, "w")

        for console in self.consoles:

            if console.fullname != self.console_label.text():
                f.write("[" + console.fullname + "]\n")

                for attribute in dir(console):

                    if attribute == "emulator" and console.emulator is not None:
                        f.write("emulator=" + console.emulator.name + "\n")
                    elif not attribute.startswith('__') and not attribute.startswith('_') and attribute != "count" and attribute != "index" and attribute != "fullname":

                        attribute_value = str(getattr(console,attribute))

                        if attribute_value != "" :

                            if attribute == "prefix":
                                attribute_value = "[" + attribute_value + "]"

                            file_attribute = attribute

                            if attribute == "shortname":
                                file_attribute = "nickname"
                            elif attribute == "custom_roms_directory":
                                file_attribute = "rom directory"
                            elif attribute == "images_directory":
                                file_attribute = "images directory"

                            f.write(file_attribute + "=" + attribute_value + "\n")
            else:
                f.write("[" + self.console_label.text() + "]\n")
                if self.shortname.text() != "":
                    f.write("nickname=" + self.shortname.text() + "\n")
                if str(self.emulator_combobox.currentText()) != "":
                    f.write("emulator=" + str(self.emulator_combobox.currentText()) + "\n")
                if self.extensions.text() != "":
                    f.write("extensions=" + self.extensions.text() + "\n")
                if self.custom_roms_directory.text() != "":
                    f.write("roms directory=" + self.custom_roms_directory.text() + "\n")
                if self.prefix.text() != "":
                    f.write("prefix=" + self.prefix.text() + "\n")
                if self.icon != "":
                    f.write("icon=" + self.icon.text() + "\n")
                if self.images_directory.text() != "":
                    f.write("images directory=" + self.images_directory.text() + "\n")
            f.write("\n")
        f.close()

    def find_console(self, name):
        for c in self.consoles:
            if c.fullname == name:
                return c
        return None

    def on_edit_console(self, console):
        if console is None:
            return
        icon = console.icon
        self.console_label.setText(console.fullname)
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
