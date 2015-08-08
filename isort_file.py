import os
import sys

import sublime
import sublime_plugin

from .isort import SortImports

sys.path.append(os.path.dirname(__file__))


class IsortCommand(sublime_plugin.TextCommand):

    def get_region(self):
        selection = self.view.sel()[0]
        if selection.empty():
            return sublime.Region(0, self.view.size())

        begin_line, begin_column = self.view.rowcol(selection.begin())
        end_line, end_column = self.view.rowcol(selection.end())
        return sublime.Region(
            self.view.text_point(begin_line, 0),
            self.view.text_point(end_line, 0)
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

    def get_settings(self):
        profile = sublime.active_window().active_view().settings().get("isort")
        return profile or {}

    def run(self, edit):
        current_positions = self.get_positions()

        this_contents = self.get_buffer_contents()
        settings = {
            'settings_path': os.path.dirname(self.view.file_name())
        }
        settings.update(self.get_settings())

        sorted_imports = SortImports(
            file_contents=this_contents,
            **settings
        ).output
        self.view.replace(edit, self.get_region(), sorted_imports)

        # Our sel has moved now..
        remove_sel = self.view.sel()[0]
        self.view.sel().subtract(remove_sel)
        self.set_cursor_back(current_positions)
