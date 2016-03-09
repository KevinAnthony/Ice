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
from ice import consoles
from ice import paths

from pysteam import paths as steam_paths
from pysteam import steam as steam_module

import pygtk
pygtk.require('2.0')
import gtk

STEAM_CHECK_SKIPPED_WARNING = """\
Not checking whether Steam is running. Any changes made may be overwritten \
when Steam exits.\
"""

class GraphicalRunner(object):
  def __init__(self,steam, filesystem, app_settings,options):
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

    roms = self.rom_finder.roms_for_consoles(self.app_settings.consoles)
    self.__init__gui()
    gtk.main()

  def __init__gui(self):
    self.window = gtk.Window()
    self.window.connect("delete_event", self.delete_event)
    self.window.connect("destroy", self.destroy)
    #self.window.set_border_width(10)
    self.window.set_default_size(800,600)
    #self.window.set_resizable(True)
    vbox = gtk.VBox(True,0)
    label = gtk.Label("Hello, ICE!")
    vbox.pack_start(label)
    button = gtk.Button("The Pudding Factory is on fire!")
    vbox.pack_start(button)
    self.window.add(vbox)
    self.window.show_all()


  def delete_event(self, widget, event, data=None):
    print "delete event occurred"
    return False

  def destroy(self, widget, data=None):
      print "destroy signal occurred"
      gtk.main_quit()
      exit(0)
