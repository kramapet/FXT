import importlib


class BaseLoader:
	"""Import and return class/attribute

	Keyword arguments:
	classname -- the absolute path to class

	Exceptions:
	ImportError -- when attempt to load class 
				   without specified module/package
	"""
	def load(self, classname):
		parts = classname.split('.')

		if len(parts) < 2:
			raise ImportError('Class name "{}" cannot be found.'.format(classname))
		else:
			module_name = '.'.join(parts[:-1])
			class_name = parts[-1]

			return getattr(importlib.import_module(module_name), class_name)
