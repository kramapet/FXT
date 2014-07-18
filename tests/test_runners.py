import unittest

from FXT.runners import CliRunner

class MockBrokerWithAnnotation:
	def __init__(self, account_balance: int, margin: float):
		pass

class MockBrokerWithoutAnnotation:
	def __init__(self, account_balance, margin):
		pass

class MockModel:
	def __init__(self, instrument: list):
		pass

class MockLoader:
	def load(self, classname):
		classes = {
			'FXT.brokers.BaseBrokerWithout' : MockBrokerWithoutAnnotation,
			'FXT.brokers.BaseBroker': MockBrokerWithAnnotation,
			'FXT.models.BaseModel': MockModel
		}

		return classes[classname]

class TestCliRunner(unittest.TestCase):

	def test_cli(self):
		options = [
			'FXT.brokers.BaseBroker',
			'FXT.models.BaseModel',
			'--broker-account-balance', '2500',
			'--broker-margin', '0.321',
			'--model-instrument', 'USD,EUR'
		]

		r = CliRunner(MockLoader())
		parsed = r.parse_arguments(options)

		self.assertEqual(parsed.broker_account_balance, 2500)
		self.assertEqual(parsed.broker_margin, 0.321)
		self.assertEqual(parsed.model_instrument, ['USD','EUR'])
