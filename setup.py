from setuptools import setup

setup(
	name='FXT',
	version='0.2.dev',
	description='ForeX Trading platform',
	url='https://github.com/kramapet/FXT',
	license='GPL',
	author='',
	author_email='',
	packages=['FXT'],
	entry_points={
		'console_scripts': [
			'fxt = FXT.runners:start_cli_runner'
		]
	}
)
