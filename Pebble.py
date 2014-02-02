import sublime, sublime_plugin
import subprocess
import os

class pebblebuild(sublime_plugin.WindowCommand):
	def run(self):
		cmd = ["pebble", "build"]
		self.window.run_command("exec", { "cmd": cmd })

class pebbleclean(sublime_plugin.WindowCommand):
	def run(self):
		cmd = ["pebble", "clean"]
		self.window.run_command("exec", { "cmd": cmd })

class pebbleinstall(sublime_plugin.WindowCommand):
	def run(self):
		cmd = ["pebble", "install"]
		self.window.run_command("exec", { "cmd": cmd })

class pebblescreenshot(sublime_plugin.WindowCommand):
	def run(self):
		cmd = ["pebble", "screenshot"]
		self.window.run_command("exec", { "cmd": cmd })