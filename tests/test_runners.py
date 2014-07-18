import unittest

from datetime import datetime
from FXT.runners import CliRunner

class MockBrokerWithAnnotation:
	def __init__(self, account_balance: int, margin: float, start_date: datetime):
		pass

class MockBrokerWithoutAnnotation:
	def __init__(self, account_balance, margin, start_date):
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

	def test_parse_arguments(self):
		options = [
			'FXT.brokers.BaseBroker',
			'FXT.models.BaseModel',
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

		options[0] = 'FXT.brokers.BaseBrokerWithout'
		parsed = r.parse_arguments(options)
		self.assertEqual(parsed.broker_account_balance, '2500')
		self.assertEqual(parsed.broker_margin, '0.321')
