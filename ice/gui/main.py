"""
gui.py

Created by Scott on 2016-03-08.
Copyright (c) 2016 Kevin Anthony. All rights reserved.
"""

from ice.logs import logger
from ice.parsing.rom_parser import ROMParser
from ice.rom_finder import ROMFinder
from ice.error.env_checker_error import EnvCheckerError
from ice.environment_checker import EnvironmentChecker
from ice.gui.emulators import EmulatoreGui
from ice.gui.consoles import ConsoleGui
from ice import consoles
from ice import paths

from pysteam import paths as steam_paths
from pysteam import steam as steam_module

import sys
from PyQt5 import Qt, QtGui, QtWidgets, QtCore


STEAM_CHECK_SKIPPED_WARNING = """\
Not checking whether Steam is running. Any changes made may be overwritten \
when Steam exits.\
"""


class GraphicalRunner(QtWidgets.QMainWindow):
  def __init__(self, steam, filesystem, app_settings,options):
    self.app = Qt.QApplication(sys.argv)
    QtWidgets.QMainWindow.__init__(self)
    self.steam = steam
    self.filesystem = filesystem

    is_user_context = lambda context: context.user_id != 'anonymous'
    self.users = filter(is_user_context, steam_module.local_user_contexts(self.steam))

    logger.debug("Initializing Ice")

    self.app_settings = app_settings

    parser = ROMParser()
    self.rom_finder = ROMFinder(app_settings.config, filesystem, parser)
    self.options = options

  def validate_environment(self, skip_steam_check):
    """
    Validate that the current environment meets all of Ice's requirements.
    """
    with EnvironmentChecker(self.filesystem) as env_checker:
      if not skip_steam_check:
        # If Steam is running then any changes we make will be overwritten
        env_checker.require_program_not_running("Steam")
      else:
        logger.warning(STEAM_CHECK_SKIPPED_WARNING)
      # I'm not sure if there are situations where this won't exist, but I
      # assume that it does everywhere and better safe than sorry
      env_checker.require_directory_exists(self.steam.userdata_directory)
      # This is used to store history information and such
      env_checker.require_directory_exists(paths.application_data_directory())

      for console in self.app_settings.consoles:
        # Consoles assume they have a ROMs directory
        env_checker.require_directory_exists(consoles.console_roms_directory(self.app_settings.config, console))

      for user in self.users:
        # If the user hasn't added any grid images on their own then this
        # directory wont exist, so we require it explicitly here
        env_checker.require_directory_exists(steam_paths.custom_images_directory(user))
        # And it needs to be writable if we are going to save images there
        env_checker.require_writable_path(steam_paths.custom_images_directory(user))
  def run(self):
    if self.steam is None:
      logger.error("Cannot run Ice because Steam doesn't appear to be installed")
      return

    logger.info("=========== Starting Ice ===========")
    try:
      self.validate_environment(self.options.skip_steam_check)
    except EnvCheckerError as e:
      logger.info("Ice cannot run because of issues with your system.\n")
      logger.info("* %s" % e.message)
      logger.info("\nPlease resolve these issues and try running Ice again")
      return

    self.__roms = self.rom_finder.roms_for_consoles(self.app_settings.consoles)
    self.__init__gui()
    self.show()
    sys.exit(self.app.exec_())

  def __init__gui(self):
    #setup window
    self.setGeometry(200,200,800, 600)
    self.resizeEvent = self.on_resize
    #Setup StatusBar
    self.statusBar = QtWidgets.QStatusBar()#self.statusBar().showMessage()
    self.setStatusBar(self.statusBar)
    self.statusBar.showMessage(str.format("{0} roms found", len(self.__roms)))
    self.statusBar.resizeEvent = self.on_resize

    #Setup Toolbar
    self.toolBar = QtWidgets.QToolBar(self)
    self.addToolBar(self.toolBar)
    self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
    self.toolBar.resizeEvent = self.on_resize

    emulatorAction = QtWidgets.QAction(self)
    emulatorAction.setIcon(QtGui.QIcon("../icon.ico"))
    emulatorAction.setIconText("Emulators")
    emulatorAction.setShortcut('Ctrl+E')
    emulatorAction.triggered.connect(self.on_emulators_pressed)
    self.toolBar.addAction(emulatorAction)

    consoleAction = QtWidgets.QAction(self)
    consoleAction.setIcon(QtGui.QIcon("../icon.ico"))
    consoleAction.setIconText("Console")
    consoleAction.setShortcut('Ctrl+S')
    consoleAction.triggered.connect(self.on_consoles_pressed)
    self.toolBar.addAction(consoleAction)

    self.toolBar.addSeparator()

    runAction = QtWidgets.QAction(self)
    runAction.setIcon(QtGui.QIcon("../icon.ico"))
    runAction.setIconText("Update Steam")
    runAction.setShortcut('Ctrl+R')
    runAction.triggered.connect(self.on_run_pressed)
    self.toolBar.addAction(runAction)

    #Setup Main Widget
    self.centralWidget = QtWidgets.QWidget(self)
    self.centralWidget.setMaximumWidth(16777215)
    self.centralWidget.setMaximumHeight(16777215)
    self.centralWidget.setContentsMargins(0,0,0,0)
    self.centralWidget.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred))
    self.centralWidget.setGeometry(0,0 ,self.width(),self.height())

    #setup layout
    layout = QtWidgets.QVBoxLayout(self.centralWidget)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)

    #setup table
    self.romTable = RomTableWidget(self.__roms)
    layout.addWidget(self.romTable)

    #setup dialogs
    self.emulators = EmulatoreGui(self, self.app_settings)
    self.consoles = ConsoleGui(self, self.app_settings)

  @QtCore.pyqtSlot()
  def on_emulators_pressed(self):
    self.emulators.exec_()

  @QtCore.pyqtSlot()
  def on_consoles_pressed(self):
    self.consoles.exec_()

  def on_run_pressed(self):
    pass

  def on_resize(self, event):
    print event
    tbHeight = self.toolBar.height()
    sbHeight = self.statusBar.height()
    # This line may seem strange but basically we need need to move the central Widget down the height of the
    # ToolBar and we want it to be the height of the window less the heights of the ToolBar and StatusBar
    self.centralWidget.setGeometry(0, tbHeight , self.width(), self.height() - sbHeight - tbHeight)

  def delete_event(self, widget, event, data=None):
    print "delete event occurred"
    return False

  def destroy(self, widget, data=None):
      print "destroy signal occurred"
     # gtk.main_quit()
      exit(0)

class RomTableWidget(QtWidgets.QTableWidget):
    def __init__(self, roms, *args):
      QtWidgets.QTableWidget.__init__(self, *args)
      self.__roms = roms
      self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)

      self.insertColumn(0)
      self.insertColumn(1)
      self.insertColumn(2)
      self.setmydata()
      self.setHorizontalHeaderLabels(['Name', 'Console','Path',])
      self.resizeColumnsToContents()
      self.resizeRowsToContents()
      self.setSortingEnabled(True)



    def updateFromDict(self, aDict):
        self.data.clear()
        self.data.update(aDict)

        self.setmydata()

    def setmydata(self):
      for n, rom in enumerate(self.__roms):
        name = rom.name
        console = rom.console.shortname
        path = rom.path
        nameItem = QtWidgets.QTableWidgetItem(name)
        consoleItem = QtWidgets.QTableWidgetItem(console)
        pathItem = QtWidgets.QTableWidgetItem(path)
        self.insertRow(n)
        self.setItem(n, 0, nameItem)
        self.setItem(n, 1, consoleItem)
        self.setItem(n, 2, pathItem)
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
