import os
import sys

import sublime
import sublime_plugin

from .isort import SortImports

sys.path.append(os.path.dirname(__file__))

PACKAGE_NAME = "importsort"
STATUS_KEY = "sublk"
ISORT_ON_SAVE_VIEW_SETTING = "importsort.isort_on_save"
SETTINGS_FILE_NAME = "importsort.sublime-settings"
SETTINGS_NS_PREFIX = "{}.".format(PACKAGE_NAME)
KEY_ERROR_MARKER = "__KEY_NOT_PRESENT_MARKER__"
CONFIG_OPTIONS = [
    "isort_on_save"
]


def is_python(view):
    return view.match_selector(0, "source.python")


def get_settings(view):
    flat_settings = view.settings()
    global_settings = sublime.load_settings(SETTINGS_FILE_NAME)
    settings = {}

    for k in CONFIG_OPTIONS:
        # check sublime "flat settings"
        value = flat_settings.get(SETTINGS_NS_PREFIX + k, KEY_ERROR_MARKER)
        if value != KEY_ERROR_MARKER:
            settings[k] = value
            continue

        #  check plugin/user settings
        settings[k] = global_settings.get(k)

    return settings


class IsortCommand(sublime_plugin.TextCommand):
    def is_enabled(self):
        return is_python(self.view)

    def get_region(self):
        selection = self.view.sel()[0]
        if selection.empty():
            return sublime.Region(0, self.view.size())

        begin_line, begin_column = self.view.rowcol(selection.begin())
        end_line, end_column = self.view.rowcol(selection.end())
        return sublime.Region(
            self.view.text_point(begin_line, 0),
            self.view.text_point(end_line, 0),
        )

    def get_buffer_contents(self):
        return self.view.substr(self.get_region())

    def set_cursor_back(self, begin_positions):
        for pos in begin_positions:
            self.view.sel().add(pos)

    def get_positions(self):
        pos = []
        for region in self.view.sel():
            pos.append(region)
        return pos

    def run(self, edit):
        current_positions = self.get_positions()

        this_contents = self.get_buffer_contents()
        settings = {"settings_path": os.path.dirname(self.view.file_name())}
        settings.update(get_settings(self.view))

        sorted_imports = SortImports(
            file_contents=this_contents, **settings
        ).output
        self.view.replace(edit, self.get_region(), sorted_imports)

        # Our sel has moved now..
        remove_sel = self.view.sel()[0]
        self.view.sel().subtract(remove_sel)
        self.set_cursor_back(current_positions)


class IsortOnSaveCommand(sublime_plugin.TextCommand):
    def is_enabled(self):
        return is_python(self.view)

    is_visible = is_enabled

    def run(self, edit):
        view = self.view

        settings = get_settings(view)
        current_state = settings["isort_on_save"]
        next_state = not current_state

        # A setting set on a particular view overules all other places where
        # the same setting could have been set as well. E.g. project settings.
        # Now, we first `erase` such a view setting which is luckily an
        # operation that never throws, and immediately check again if the
        # wanted next state is fulfilled by that side effect.
        # If yes, we're almost done and just clean up the status area.
        view.settings().erase(ISORT_ON_SAVE_VIEW_SETTING)
        if get_settings(view)["isort_on_save"] == next_state:
            view.erase_status(STATUS_KEY)

        # Otherwise, we set the next state, and indicate in the status bar
        # that this view now deviates from the other views.
        view.settings().set(ISORT_ON_SAVE_VIEW_SETTING, next_state)
        view.set_status(
            STATUS_KEY, "isort: {}".format("on" if next_state else "off")
        )


class IsortEventListener(sublime_plugin.EventListener):
    def on_pre_save(self, view):
        """use blackd at saving time
        Cannot be async since black should be run before save"""
        if get_settings(view).get("isort_on_save"):
            view.run_command("isort")
