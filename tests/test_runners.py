import unittest

from datetime import datetime
from FXT.runners import CliRunner

class MockBrokerWithAnnotation:
	def __init__(self, account_balance: int, margin: float, start_date: datetime):
		pass

class MockBrokerWithDefaults:
	def __init__(self, account_balance: int, margin: float, start_date: datetime = '1989-07-20 12:00:00'):
		pass

class MockBrokerWithoutAnnotation:
	def __init__(self, account_balance, margin, start_date):
		pass

class MockRenderer:
	def __init__(self):
		pass

class MockModel:
	def __init__(self, instrument: list):
		pass

class MockLoader:
	def load(self, classname):
		classes = {
			'FXT.brokers.BaseBrokerWithout' : MockBrokerWithoutAnnotation,
			'FXT.brokers.BaseBroker': MockBrokerWithAnnotation,
			'FXT.brokers.BaseBrokerDefault': MockBrokerWithDefaults,
			'FXT.models.BaseModel': MockModel,
			'FXT.renderers.BaseRenderer': MockRenderer
		}

		return classes[classname]

class TestCliRunner(unittest.TestCase):

	def test_parse_arguments(self):
		options = [
			'--broker', 'FXT.brokers.BaseBroker',
			'--model', 'FXT.models.BaseModel',
			'--renderer', 'FXT.renderers.BaseRenderer',
			'--broker-account-balance', '2500',
			'--broker-margin', '0.321',
			'--broker-start-date', '1989-07-20 23:00:12',
			'--model-instrument', 'USD,EUR'
		]

		r = CliRunner()
		r.loaders.append(MockLoader())
		parsed = r.parse_arguments(options)

		self.assertEqual(parsed.broker_account_balance, 2500)
		self.assertEqual(parsed.broker_margin, 0.321)
		self.assertEqual(parsed.broker_start_date, datetime(1989, 7, 20, 23, 0, 12))
		self.assertEqual(parsed.model_instrument, ['USD','EUR'])

		options[1] = 'FXT.brokers.BaseBrokerWithout'
		parsed = r.parse_arguments(options)
		self.assertEqual(parsed.broker_account_balance, '2500')
		self.assertEqual(parsed.broker_margin, '0.321')

		options[1] = 'FXT.brokers.BaseBrokerDefault'		
		options.remove('--broker-start-date')
		options.remove('1989-07-20 23:00:12')
		parsed = r.parse_arguments(options)
		self.assertEqual(parsed.broker_account_balance, 2500)
		self.assertEqual(parsed.broker_margin, 0.321)
		self.assertEqual(parsed.broker_start_date, datetime(1989, 7, 20, 12, 0, 0))
