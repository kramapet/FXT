from argparse import ArgumentParser
from datetime import datetime

class BaseRunner:

	def run(self, broker, model, renderer):
		"""Run app life cycle

		Keyword arguments:
		broker -- FXT.brokers.BaseBroker
		model  -- FXT.models.BaseModel
		renderer -- FXT.renderers.BaseRenderer
		"""
		while broker.has_tick():
			broker.before_tick()
			model.before_tick()
			model.process_tick(broker.get_tick())
			model.after_tick()
			broker.after_tick()

		transaction = broker.get_transactions()
		broker_info = broker.get_info()
		model_info = model.get_info()

		renderer.process(transactions, broker_info, model_info)

"""CliRunner - class for running app from cli

TODO:
	Add support for entity as another dependency
"""
class CliRunner(BaseRunner):
	
	def __init__(self):
		self.loaders = list()
		self.type_callbacks = {
			list: lambda arg: arg.split(','),
			datetime: lambda arg: datetime.strptime(arg, '%Y-%m-%d %H:%M:%S')
		}	

	def parse_arguments(self, args):
		"""Parse arguments

		Keyword arguments:
		args -- <list> arguments
		"""
		entities = ('broker', 'model', 'renderer')
		parser = ArgumentParser()

		# add entities as required arguments
		for ent in entities:
			parser.add_argument('--' + ent, '-' + ent[0], help=ent + ' class', required=True)

		parsed = parser.parse_known_args(args)[0]

		entities_class = dict() # entity: class
		for ent in entities:
			entities_class[ent] = self.load_class(getattr(parsed, ent))
			self.add_entity_arguments(parser, ent, entities_class[ent])

	
		parsed = parser.parse_args(args)

		for ent in entities:
			# replace classnames by class in parsed arguments
			setattr(parsed, ent, entities_class[ent])

		return parsed

	def load_class(self, cls):
		"""Try to load class from registered loaders

		Keyword arguments:
		classname -- classname
		"""
		
		"""Loader tries to load a class 
		if package is successfully loaded and class returned
		end of loop and class is returned from function
		if loader cannot load/find particular classname
		then loader raises ImportError, that exception
		is caught and next loader give a try"""
		for loader in self.loaders:
			try:
				return loader.load(cls)
			except ImportError: 
				pass 
			

		raise ImportError('Class {} not found'.format(cls))
	

	def add_entity_arguments(self, parser, entity, entity_class):
		"""Add entity arguments

		Check if constructor of entity class has annotated
		arguments to use proper type, non-annotated arguments
		will be filled as strings

		Keyword arguments:
		parser -- <ArgumentParser>
		entity -- <string> {model,broker,renderer,...}
		entity_class -- <class>
		"""
		
		# constructor is not defined
		if not hasattr(entity_class, '__init__'):
			return

		code = entity_class.__init__.__code__

		# entity constructor has not any argument to pass
		# just self
		if code.co_argcount < 2: 
			return

		# return argument names without 'self'
		init_args = code.co_varnames[1:]
		init_annot = entity_class.__init__.__annotations__
		init_defaults = dict()

		if entity_class.__init__.__defaults__ is not None:
			# get dict with default values - varname: default_value
			init_defaults = dict(zip(reversed(init_args), reversed(entity_class.__init__.__defaults__)))
		for arg in init_args:
			kwargs = dict(required=True,default=None)
			# build long posix argument name
			arg_name = '--' + entity + '-' + arg.replace('_','-')
			# set default type to string
			arg_type = str
			
			if arg in init_annot:
				arg_type = self.get_type_callback(init_annot[arg])

			if arg in init_defaults:
				kwargs['required'] = False
				kwargs['default'] = init_defaults[arg]


			parser.add_argument(arg_name, type=arg_type, **kwargs)

	def get_type_callback(self, arg_type):
		"""Get callback to convert argument

		Keyword arguments:
		arg_type -- argument type
		"""
		if arg_type in self.type_callbacks:
			return self.type_callbacks[arg_type]

		return arg_type

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
