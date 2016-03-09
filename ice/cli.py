"""
command_line_runner.py

Created by Scott on 2014-08-14.
Copyright (c) 2014 Scott Rice. All rights reserved.
"""

import argparse

from pysteam.steam import get_steam, Steam

import decorators
import debug
import settings

from logs import logger
from filesystem import RealFilesystem
from tasks import  TaskEngine, LaunchSteamTask, LogAppStateTask, SyncShortcutsTask, UpdateGridImagesTask
from gui import GraphicalRunner

class CommandLineRunner(object):

  def __init__(self, steam=None, filesystem=None):
    self.steam = steam
    self.filesystem = RealFilesystem() if filesystem is None else filesystem

  def get_command_line_args(self, argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('pdebug', type=bool, nargs='?', help="Pastes debug logs to pastebin to include with bug reports.")
    parser.add_argument('--skip-steam-check', action='store_true', help="Skips checking whether Steam is running")
    parser.add_argument('--launch-steam', action='store_true', help="Launches Steam after the shortcuts have been synced and its safe to do so")
    # Config options
    parser.add_argument('-c', '--config', type=str, default=None)
    parser.add_argument('-C', '--consoles', type=str, default=None)
    parser.add_argument('-e', '--emulators', type=str, default=None)
    # Debugging options
    parser.add_argument('-d', '--dry-run', action='store_true')
    parser.add_argument('-g', '--gui', action='store_true', help="Launches app with experimental gui")
    return parser.parse_args(argv)

  def should_use_user_override(self, override):
    if override is None:
      return False
    if override == "":
      return False
    if not self.filesystem.path_exists(override):
      logger.warning("config.txt specifies a Steam userdata directory that doesn't exist. Ignoring.")
      return False
    return False

  def get_steam(self, config):
    override = config.userdata_directory
    if self.should_use_user_override(override):
      return Steam(override)

    if self.steam is not None:
      return self.steam

    return get_steam()

  def tasks_for_options(self, app_settings, options):
    tasks = [
      LogAppStateTask(app_settings),
      SyncShortcutsTask(app_settings),
    ]

    if options.launch_steam:
      tasks = tasks + [ LaunchSteamTask() ]

    tasks = tasks + [ UpdateGridImagesTask(app_settings) ]
    return tasks

  @decorators.catch_exceptions("An exception occurred while running Ice")
  def run(self, argv):
    options = self.get_command_line_args(argv[1:])

    if options.pdebug is True:
      debug.paste_debug_logs()
      return

    app_settings = settings.load_app_settings(self.filesystem, file_overrides = {
        'config.txt': options.config,
        'consoles.txt': options.consoles,
        'emulators.txt': options.emulators,
    })
    if options.gui:
      gui = GraphicalRunner(
        self.get_steam(app_settings.config),
        self.filesystem,
        app_settings,
        options
      )
      gui.run()
    else:
      engine = TaskEngine(
        self.get_steam(app_settings.config),
        filesystem = self.filesystem,
        app_settings = app_settings,
      )
      engine.run(
        tasks = self.tasks_for_options(app_settings, options),
        skip_steam_check=options.skip_steam_check,
        dry_run=options.dry_run
      )
