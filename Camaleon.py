# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import fnmatch
import os
import random
import sublime, sublime_plugin

PLUGIN_NAME = "Camaleón"
ST_PREFERENCES = "Preferences.sublime-settings"
PLUGIN_PREFERENCES = "Camaleon.sublime-settings"
PLUGIN_STATE = "Camaleon.selected-preset"

def is_st3():
    return int(sublime.version()) >= 3000

def print_unicode(*args, **kwargs):
    if not is_st3():
        # we explicitly encode everything to UTF-8 since Mac OS' system Python
        # seems to try ASCII otherwise
        print(*(s.encode("utf-8") for s in args), **kwargs)
    else:
        # we have Python 3 so everyone should handle Unicode properly now
        print(*args, **kwargs)

# check if a resource exists, which may either be a plain file name or a full
# path starting with 'Packages/', using '/' as a platform-independent path sep
def check_resource_exists(name):
    if name.startswith("Packages/"):
        if is_st3():
            # ST3
            try:
                sublime.load_resource(name)
            except IOError:
                return False
            return True
        else:
            # ST2 compatibility
            fpath = os.path.normpath(os.path.join(sublime.packages_path(),
                                                  os.pardir,
                                                  name.replace("/", os.sep)))
            return os.path.isfile(fpath)
    else:
        return len(find_resources(name)) > 0

# semi-complete ST2 version of sublime.find_resources
def _st2_find_resources(pattern):
    pkgpath = sublime.packages_path()
    for dirpath, dirnames, filenames in os.walk(pkgpath):
        for filename in filenames:
            if fnmatch.fnmatch(filename, pattern):
                path = os.path.relpath(dirpath, pkgpath).replace(os.sep, "/")
                yield "Packages/%s/%s" % (path, filename)

# find_resources compatibility wrapper
def find_resources(pattern):
    if is_st3():
        # ST3
        return sublime.find_resources(pattern)
    else:
        # ST2 compatibility
        return list(_st2_find_resources(pattern))

def friendly_name(name):
    return name.rsplit("/", 1)[-1].rsplit(".", 1)[0]


# set UI theme and colour scheme, checking if they exist
def set_theme(chrome_theme=None, color_scheme=None):
    sublime_settings = sublime.load_settings(ST_PREFERENCES)
    if chrome_theme is not None:
        if check_resource_exists(chrome_theme):
            sublime_settings.set("theme", chrome_theme)
        else:
            print_unicode("%s: theme '%s' doesn't seem to be installed"
                          % (PLUGIN_NAME, friendly_name(chrome_theme)))
    if color_scheme is not None:
        if check_resource_exists(color_scheme):
            sublime_settings.set("color_scheme", color_scheme)
        else:
            print_unicode("%s: colour scheme '%s' doesn't seem to be installed"
                          % (PLUGIN_NAME, friendly_name(color_scheme)))
    sublime.save_settings(ST_PREFERENCES)

# load a given settings preset
def load_preset(plugin_settings, plugin_state, idx):
    try:
        chrome_theme = plugin_settings.get("camaleon")[idx][0]
        color_scheme = plugin_settings.get("camaleon")[idx][1]
    except:
        # that didn't work
        return
    set_theme(chrome_theme, color_scheme)
    plugin_state.set("current", idx)
    sublime.save_settings(PLUGIN_STATE)

# pick index for next, previous and random preset respectively
def get_next_preset_idx(current, num):
    return current + 1 if current + 1 < num else 0

def get_prev_preset_idx(current, num):
    return current - 1 if current > 0 else num - 1

def get_random_preset_idx(num):
    return random.randrange(num)


class CamaleonCommand(sublime_plugin.WindowCommand):
    def run(self, type="next"):
        plugin_settings = sublime.load_settings(PLUGIN_PREFERENCES)
        plugin_state = sublime.load_settings(PLUGIN_STATE)
        try:
            current = int(plugin_state.get("current", 0))
        except:
            # 'current' seems invalid, reset it
            print_unicode("%s: 'current' setting seems invalid, resetting to 0"
                          % PLUGIN_NAME)
            current = 0
        try:
            num = len(plugin_settings.get("camaleon"))
        except:
            # the preset object seems entirely invalid, we can't do anything
            print_unicode("%s: invalid preset settings" % PLUGIN_NAME)
            return

        if type == "previous":
            next_idx = get_prev_preset_idx(current, num)
        elif type == "random":
            next_idx = get_random_preset_idx(num)
        else:
            next_idx = get_next_preset_idx(current, num)

        load_preset(plugin_settings, plugin_state, next_idx)

class CamaleonRandomColourSchemeCommand(sublime_plugin.WindowCommand):
    def run(self):
        all_themes = find_resources("*.tmTheme")
        color_scheme = random.choice(all_themes)
        set_theme(None, color_scheme)
        sublime.status_message("%s: picked random colour scheme '%s'" %
                               (PLUGIN_NAME, friendly_name(color_scheme)))
