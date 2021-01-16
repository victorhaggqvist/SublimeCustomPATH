import logging
import os

import better_settings
import sublime
import sublime_plugin

PLUGIN_ID = "CustomPATH"
ON_CHANGE_HANDLER_KEY = "CUSTOM_PATH_ON_CHANGE"
LOGGER = logging.getLogger(PLUGIN_ID)


def _load_settings():
    return better_settings.load_for(__package__, PLUGIN_ID)


def plugin_loaded():
    # Sublime's default path on linux is
    # /usr/local/sbin:/usr/local/bin:/usr/bin:/usr/lib/jvm/default/bin:/usr/bin/site_perl:/usr/bin/vendor_perl:/usr/bin/core_perl
    settings = _load_settings()

    settings.clear_on_change(ON_CHANGE_HANDLER_KEY)
    settings.add_on_change(ON_CHANGE_HANDLER_KEY, plugin_loaded)

    path = settings.get("PATH", "")
    if len(path) == 0:
        return

    original_path = os.environ.get(
        "CUSTOM_PATH_ORIGINAL_PATH", default=os.environ["PATH"]
    )

    LOGGER.info("Original Path: %s" % original_path)

    os.environ["CUSTOM_PATH_ORIGINAL_PATH"] = original_path

    if path in original_path:  # avoid inserting path multiple times
        LOGGER.info("Path loaded: %s" % original_path)
        return

    override = settings.get("override", False)
    if override:
        os.environ["PATH"] = path
    else:
        append_front = settings.get("append_front")
        if append_front:
            os.environ["PATH"] = path + os.pathsep + original_path
        else:
            os.environ["PATH"] = original_path + os.pathsep + path

    LOGGER.info("Path loaded: %s" % os.environ["PATH"])


def plugin_unloaded():
    settings.clear_on_change(ON_CHANGE_HANDLER_KEY)


class CustomPathOpenSettings(sublime_plugin.WindowCommand):
    def __init__(self, *args, **kwargs):
        sublime_plugin.WindowCommand.__init__(self, *args, **kwargs)

    def run(self, scope=None):
        _load_settings().open_settings(self.window, scope)
