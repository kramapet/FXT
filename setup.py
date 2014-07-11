from setuptools import setup
from setuptools.command.install import install

from os import path
from subprocess import call

class UpdateSubmodules(install):
	def run(self):
		"""Hook to update git submodules on install"""
		if path.exists('.git'):
			call(['git', 'submodule', 'init'])
			call(['git', 'submodule', 'update'])

		install.run(self)

setup(
	name='FXT',
	version='0.2.dev',
	description='ForeX Trading platform',
	url='https://github.com/kramapet/FXT',
	license='GPL',
	author='',
	author_email='',
	packages=['FXT', 'FXT.brokers', 'FXT.models', 'FXT.thirdparty.oandapy'],
	install_requires=['pandas', 'matplotlib'],
	cmdclass={
		'install': UpdateSubmodules
	},
	entry_points={
		'console_scripts': [
			'fxt = FXT.runners:start_cli_runner'
		]
	}
)
