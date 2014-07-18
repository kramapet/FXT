from argparse import ArgumentParser

class BaseRunner:

	def run(self):
		while self.broker.has_tick():
			self.model.beforeTick()
			self.model.processTick(self.broker.get_tick())
			self.model.afterTick()
			self.broker.afterTick()

		self.renderer.process(self.broker.get_transactions(), self.broker.get_info(), self.model.get_info())



class CliRunner(BaseRunner):
	
	def __init__(self, loader):
		self.loader = loader
		self.type_callbacks = {
			list: self.__parse_type_list
		}	

	def parse_arguments(self, args):
		"""Parse arguments

		Keyword arguments:
		args -- <list> arguments
		"""
		entities = ('broker', 'model')

		broker_class = self.loader.load(args[0])
		model_class = self.loader.load(args[1])
		parser = ArgumentParser()
		parser.add_argument('broker', help='Broker class')
		parser.add_argument('model', help='Model class')

		for entity in entities:
			self.__add_entity_arguments(parser, entity, broker_class)
			self.__add_entity_arguments(parser, entity, model_class)


		return parser.parse_args(args)

	def __add_entity_arguments(self, parser, entity, entity_class):
		"""Add entity arguments

		Check if constructor of entity class has annotated
		arguments to use proper type, non-annotated arguments
		will be filled as strings

		Keyword arguments:
		parser -- <ArgumentParser>
		entity -- <string> {model,broker,renderer}
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

		for arg in init_args:
			# build long posix argument name
			arg_name = '--' + entity + '-' + arg.replace('_','-')
			# set default type to string
			arg_type = str
			
			if arg in init_annot:
				arg_type = self.__get_type_callback(init_annot[arg])

			parser.add_argument(arg_name, type=arg_type)

	def __instantiate_entity(self, entity, entity_class, args):
		pass

	def __parse_type_list(self, arg):
		"""Parse argument type of list"""
		return arg.split(',')

	def __get_type_callback(self, arg_type):
		"""Get function responsible for converting argument
		to annotated argument

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
