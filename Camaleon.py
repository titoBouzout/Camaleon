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

		import codecs
		#check for soda theme if we are going to switch to soda
		if s.get('camaleon')[next][0].find('Soda') == 0 and False == os.path.isdir(os.path.join(sublime.packages_path(), 'Theme - Soda')):
			pass
		else:
			path = os.path.join(sublime.packages_path(), 'User', 'Global.sublime-settings')
			content = codecs.open(path, 'r', 'utf-8').read()
			try:
				codecs.open(path, 'w+', 'utf-8').write(content.replace(
																															s.get('camaleon')[current][0], 
																															s.get('camaleon')[next][0]
																														))
			except:
				codecs.open(path, 'w+', 'utf-8').write(content)

		# colour scheme change
		import json
		path = os.path.join(sublime.packages_path(), 'User', 'Base File.sublime-settings')
		BaseFile = json.loads(file(path, 'rb').read())
		BaseFile['color_scheme'] = s.get('camaleon')[next][1]
		s.set('current', next);
		sublime.save_settings('Camaleon.sublime-settings')
		file(path, 'wb+').write(json.dumps(BaseFile, indent=1))

class CamaleonRandomColourSchemeCommand(sublime_plugin.WindowCommand):
	def run(self, type = 'next'):
		schemes = []
		for scheme in os.listdir(os.path.join(sublime.packages_path(), 'Color Scheme - Default')):
			if scheme[-7:] == 'tmTheme':
				schemes.append(scheme)
		from random import choice
		scheme = choice(schemes)
		if scheme != '':
			import json
			path = os.path.join(sublime.packages_path(), 'User', 'Base File.sublime-settings')
			BaseFile = json.loads(file(path, 'rb').read())
			BaseFile['color_scheme'] = "Packages/Color Scheme - Default/"+scheme
			file(path, 'wb+').write(json.dumps(BaseFile, indent=1))
			sublime.status_message(u'Camaleon : Loaded colour scheme : '+scheme.decode('utf-8'))