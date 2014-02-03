import sublime, sublime_plugin
import subprocess
import os
import shlex

class PebbleCommand(sublime_plugin.WindowCommand):
	def __init__(self, *args, **kwargs):
		super(PebbleCommand, self).__init__(*args, **kwargs)
		settings = sublime.load_settings('Pebble.sublime-settings')
		self.pebble_path = settings.get('pebble_path')

	def run(self, *args, **kwargs):
		try:
			self.PROJECT_PATH = self.window.folders()[0]
			self.args = [self.pebble_path, os.path.join(self.PROJECT_PATH, 'pebble')]

			self.command = kwargs.get('command', None)
			self.args = [self.pebble_path]
			if self.command is None:
				self.window.show_input_panel('Command name w/o args:', '', self.on_command_custom, None, None)
			else:
				self.on_command(self.command)
		except IndexError:
			sublime.status_message('Please open a Pebble project')

	def on_command(self, command):
		self.args.extend(shlex.split(str(self.command)))

		self.on_done()

	def on_command_custom(self, command):
		self.args.extend(shlex.split(str(command)))
		self.on_done()

	def on_done(self):
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