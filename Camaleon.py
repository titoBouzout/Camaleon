# coding=utf8
import sublime, sublime_plugin
import os

class CamaleonCommand(sublime_plugin.WindowCommand):
	def run(self, type = 'next'):

		s = sublime.load_settings('Camaleon.sublime-settings')
		current = int(s.get('current'))

		try:
			s.get('camaleon')[current][0]
		except:
			current = 0
			try:
				s.get('camaleon')[current][0]
			except:
				return # total empty
		try:
			if type == 'next':
				s.get('camaleon')[current+1][0]
				next = current+1
			else:
				s.get('camaleon')[current-1][0]
				next = current-1
				if next < 0:
					next = len(s.get('camaleon'))-1
		except:
			try:
				if type == 'next':
					next = 0
				else:
					next = len(s.get('camaleon'))-1
				s.get('camaleon')[next][0]
			except:
				return # total empty

		# chrome change

		#check for soda theme if we are going to switch to soda
		if s.get('camaleon')[next][0].find('Soda') == 0 and False == os.path.isdir(os.path.join(sublime.packages_path(), 'Theme - Soda')):
			pass
		else:
			if int(sublime.version()) >= 2174:
				sublime_s = sublime.load_settings('Preferences.sublime-settings')
			else:
				sublime_s = sublime.load_settings('Global.sublime-settings')
			sublime_s.set('theme', s.get('camaleon')[next][0]);
			if int(sublime.version()) >= 2174:
				sublime.save_settings('Preferences.sublime-settings')
			else:
				sublime.save_settings('Global.sublime-settings')

		# colour scheme change
		if int(sublime.version()) >= 2174:
			sublime_s = sublime.load_settings('Preferences.sublime-settings')
		else:
			sublime_s = sublime.load_settings('Base File.sublime-settings')

		sublime_s.set('color_scheme', s.get('camaleon')[next][1]);
		if int(sublime.version()) >= 2174:
			sublime.save_settings('Preferences.sublime-settings')
		else:
			sublime.save_settings('Base File.sublime-settings')

		s.set('current', next);
		sublime.save_settings('Camaleon.sublime-settings')

class CamaleonRandomColourSchemeCommand(sublime_plugin.WindowCommand):
	def run(self):
		schemes = []
		for dirname, dirnames, filenames in os.walk(sublime.packages_path()):
		    for filename in filenames:
				if filename[-7:] == 'tmTheme':
					schemes.append(os.path.join(dirname, filename))
		from random import choice
		scheme = choice(schemes)
		if scheme != '':
			if int(sublime.version()) >= 2174:
				sublime_s = sublime.load_settings('Preferences.sublime-settings')
			else:
				sublime_s = sublime.load_settings('Base File.sublime-settings')

			sublime_s.set('color_scheme', scheme);

			if int(sublime.version()) >= 2174:
				sublime.save_settings('Preferences.sublime-settings')
			else:
				sublime.save_settings('Base File.sublime-settings')

			sublime.status_message(u'Camaleon : Loaded colour scheme : '+scheme.decode('utf-8'))