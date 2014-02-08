import sublime, sublime_plugin
import subprocess
import os
import shlex

settings = sublime.load_settings('Pebble.sublime-settings')

class Pref:
	def load(self):
		Pref.pebble_path = settings.get('pebble_path', 'pebble')
		Pref.pebble_phone = settings.get('pebble_phone', None)

Pref = Pref()
Pref.load()
settings.add_on_change('reload', lambda: Pref.load())

class PebbleCommand(sublime_plugin.WindowCommand):
	def __init__(self, *args, **kwargs):
		super(PebbleCommand, self).__init__(*args, **kwargs)

	def run(self, *args, **kwargs):
		try:
			self.PROJECT_PATH = self.window.folders()[0]

			if os.path.isfile("%s" % os.path.join(self.PROJECT_PATH, 'appinfo.json')):
				self.command       = kwargs.get('command', None)
				self.fill          = kwargs.get('fill', False)
				self.fill_label    = kwargs.get('fill_label', None)
				self.fields_accept = kwargs.get('fields_accept', None)
				self.args          = ['python', Pref.pebble_path]

				if self.command is None:
					self.window.show_input_panel('Command name w/o args:', '', self.on_command_custom, None, None)
				else:
					self.on_command(self.command)
			else:
				sublime.status_message('App info not found');
		except IndexError:
			sublime.status_message('Please open a Pebble project')

	def on_command(self, command):
		self.args.extend(shlex.split(str(self.command)))

		if self.fill is True:
			self.window.show_input_panel(self.fill_label, "", self.on_fill_in, None, None)
		else:
			self.on_done()

	def on_fill_in(self, fill_in):
		self.args.extend(shlex.split(str(fill_in)))

		if self.fields_accept is True:
			self.window.show_input_panel(self.fields_label, "", self.on_fields, None, None)
		else:
			self.on_done()

	def on_fields(self, fields):
		if fields != '':
			self.args.append(fields)
			self.on_done()
		else:
			self.on_done()

	def on_command_custom(self, command):
		self.args.extend(shlex.split(str(command)))
		self.on_done()

	def on_done(self):
		if self.command == 'set_pebble_phone':
			settings = sublime.load_settings('Pebble.sublime-settings')
			settings.set('pebble_phone', self.args[2])
			sublime.save_settings('Pebble.sublime-settings')
		else:
			# Add the phone IP
			self.args.append('--phone')
			self.args.append(Pref.pebble_phone)

			if os.name != 'posix':
				self.args = subprocess.list2cmdline(self.args)

			try:
				self.window.run_command('exec', {
					"cmd": self.args,
					"shell": False,
					"working_dir": self.PROJECT_PATH
				})
			except IOError:
				sublime.status_message('IOError - Command aborted') 