from abc import ABCMeta

class AbstractRunner(metaclass=ABCMeta):
	pass

class CliRunner(AbstractRunner):
	def run(self):
		print("CliRunner")


def start_cli_runner():
	"""used by setuptools. see setup.py
	installation make executable command running
	this function"""

	import logging
	
	from FXT.driver import Driver
	
	FORMAT = '%(asctime)s %(name)s: %(messages)s'
	logging.basicConfig(format=FORMAT)

	d = Driver()
	d.start()
