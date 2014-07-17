import unittest

import FXT.loaders

class TestBaseLoader(unittest.TestCase):

	def setUp(self):
		self.loader = FXT.loaders.BaseLoader()

		self.assertIsInstance(self.loader.load('xml.etree.ElementTree.Element'), type)

if __name__ == '__main__':
	unittest.main()
