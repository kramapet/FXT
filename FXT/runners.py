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

"""
class CliRunner(BaseRunner):
	
	def __init__(self):
		self.loaders = list()
		self.type_callbacks = {
			list: lambda arg: arg.split(','),
			datetime: lambda arg: datetime.strptime(arg, '%Y-%m-%d %H:%M:%S')
		}	
		self.entities_class = dict()
		self.entities_args = dict()

	def parse_arguments(self, args):
		"""Parse arguments

		Keyword arguments:
		args -- <list> arguments
		"""
		entities = [ 'broker', 'model', 'renderer' ]
		parser = ArgumentParser()

		# add entities as required arguments
		for ent in entities:
			parser.add_argument('--' + ent, '-' + ent[0], help=ent + ' class', required=True)

		parsed = parser.parse_known_args(args)[0]

		for ent in entities:
			self.entities_class[ent] = self.load_class(getattr(parsed, ent))
			self.add_entity_arguments(parser, ent, self.entities_class[ent])
	
		parsed = parser.parse_args(args)

		for ent in entities:
			setattr(self, ent, self.instantiate_entity(ent, self.entities_class[ent], parsed))

	def instantiate_entity(self, entity, cls, namespace):
		"""Instantiate entity from parsed arguments

		Keyword arguments:
		entity -- <str> entity name
		cls -- <class> entity class
		namespace -- parsed arguments
		"""
		entity_args = dict()

		if entity in self.entities_args:
			entity_args = self.entities_args[entity]
			for k in entity_args:
				if entity_args[k].startswith(':'): # it is entity
					entity_args[k] = self.instantiate_entity(k, self.entities_class[k], namespace)
				else: # regular argument
					entity_args[k] = getattr(namespace, entity_args[k])

		return cls(**entity_args)



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

		code = entity_class.__init__.__code__

		# entity constructor has not any argument to pass
		# just self
		if code.co_argcount < 2: 
			return

		# return argument names without 'self'
		init_args = code.co_varnames[1:]
		init_annot = entity_class.__init__.__annotations__
		init_defaults = dict()
		self.entities_args[entity] = dict()

		if entity_class.__init__.__defaults__ is not None:
			# get dict with default values - varname: default_value
			init_defaults = dict(zip(reversed(init_args), reversed(entity_class.__init__.__defaults__)))

		for arg in init_args:
			if arg in init_annot and self.is_entity(init_annot[arg]):
				self.entities_class[arg] = init_annot[arg]
				# new entity is marked by :, see instantiate_entity
				self.entities_args[entity][arg] = ':' + arg
				self.add_entity_arguments(parser, arg, init_annot[arg])
				continue

			kwargs = dict(required=True,default=None)
			# build long posix argument name
			arg_name = '--' + entity + '-' + arg.replace('_','-')
			# set default type to string
			arg_type = str
			
			if arg in init_annot:
				arg_type = self.get_type_callback(init_annot[arg])

			self.entities_args[entity][arg] = entity + '_' + arg

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

	def is_entity(self, ent):
		"""Return True if entity has been passed

		entity have not registered type callback
		entity is not str, int, float 

		Keyword arguments:
		ent -- entity type
		"""
		return self.get_type_callback(ent) is ent and \
				not ent in [str, int, float]

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
