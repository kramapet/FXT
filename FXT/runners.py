from abc import ABCMeta

class AbstractRunner(metaclass=ABCMeta):
	pass

class CliRunner(AbstractRunner):
	def run(self):
		print("CliRunner")


def start_cli_runner():
	"""start CliRunner, used by setuptools. see setup.py"""
	r = CliRunner()
	r.run()
