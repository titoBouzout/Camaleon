Camaleón -- quick-cycle Sublime theme and colour scheme
=======================================================
This plugin allows you to quickly cycle through a set of user-defined UI theme/
colour scheme combinations.

# Installation

Download or clone the contents of this repository to a folder named exactly as the package name into the Packages/ folder of ST.

## Usage
By default, pressing `F8` will cycle to the next preset, `Shift+F8` will switch
to the previous preset and `Alt-F8` will pick a random color scheme from all
schemes you have installed (so not just those in your presets). In addition, a
random preset can be chosen from the command palette. The other commands are
also accessible from there.

If a theme or color scheme specified in a preset is not installed in this
Sublime Text instance, the theme or color scheme respectively will not be
changed when you switch presets. The default presets are using the
[*Soda* themes][soda] so if you cycle the default presets without having these
themes installed, the color scheme will switch as intended, but your UI theme
will not change.

[soda]: https://github.com/buymeasoda/soda-theme

## Configuration
Custom presets can be configured in `Packages/User/Camaleon.sublime-settings`.
The default settings file is commented and intended to be used as a guideline;
it can be accessed from the Sublime Text menu bar, via *Preferences ->
Package Settings -> Camaleón -> Settings – Default*.

## About
The source code can be found on [GitHub][src]. There is also a [forum thread][forum].

[src]: https://github.com/titoBouzout/Camaleon
[forum]: http://www.sublimetext.com/forum/viewtopic.php?f=5&t=4435

Copyright (C) 2012 Tito Bouzout <tito.bouzout@gmail.com>
Copyright (C) 2013, 2014 Felix Krull <f_krull@gmx.de>

This license apply to all the files inside this program unless noted
different for some files or portions of code inside these files.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation. http://www.gnu.org/licenses/gpl.html

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see http://www.gnu.org/licenses/gpl.html
