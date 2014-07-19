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

class MockBrokerWithEntity:
	def __init__(self, source: MockBrokerWithDefaults):
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
			'FXT.brokers.BrokerWithEntity': MockBrokerWithEntity,
			'FXT.models.BaseModel': MockModel,
			'FXT.renderers.BaseRenderer': MockRenderer
		}

		return classes[classname]

class TestCliRunner(unittest.TestCase):

	def setUp(self):
		self.runner = CliRunner()
		self.runner.loaders.append(MockLoader())

	def test_parse_arguments_with_annotation(self):
		options = [
			'--broker', 'FXT.brokers.BaseBroker',
			'--model', 'FXT.models.BaseModel',
			'--renderer', 'FXT.renderers.BaseRenderer',
			'--broker-account-balance', '2500',
			'--broker-margin', '0.321',
			'--broker-start-date', '1989-07-20 23:00:12',
			'--model-instrument', 'USD,EUR'
		]

		parsed = self.runner.parse_arguments(options)

		self.assertEqual(parsed.broker_account_balance, 2500)
		self.assertEqual(parsed.broker_margin, 0.321)
		self.assertEqual(parsed.broker_start_date, datetime(1989, 7, 20, 23, 0, 12))
		self.assertEqual(parsed.model_instrument, ['USD','EUR'])

	def test_parse_arguments_without_annotation(self):
		options = [
			'--broker', 'FXT.brokers.BaseBrokerWithout',
			'--model', 'FXT.models.BaseModel',
			'--renderer', 'FXT.renderers.BaseRenderer',
			'--broker-account-balance', '2500',
			'--broker-margin', '0.321',
			'--broker-start-date', '1989-07-20 23:00:12',
			'--model-instrument', 'USD,EUR'
		]

		parsed = self.runner.parse_arguments(options)
		self.assertEqual(parsed.broker_account_balance, '2500')
		self.assertEqual(parsed.broker_margin, '0.321')

	def test_parse_arguments_with_default_values(self):

		options = [
			'--broker', 'FXT.brokers.BaseBrokerDefault',
			'--model', 'FXT.models.BaseModel',
			'--renderer', 'FXT.renderers.BaseRenderer',
			'--broker-account-balance', '2500',
			'--broker-margin', '0.321',
			'--model-instrument', 'USD,EUR'
		]

		parsed = self.runner.parse_arguments(options)
		self.assertEqual(parsed.broker_account_balance, 2500)
		self.assertEqual(parsed.broker_margin, 0.321)
		self.assertEqual(parsed.broker_start_date, datetime(1989, 7, 20, 12, 0, 0))

"""
	def test_parse_arguments_with_entity(self):
		options = [
			'--broker', 'FXT.brokers.BrokerWithEntity',
			'--model', 'FXT.models.BaseModel',
			'--renderer', 'FXT.renderers.BaseRenderer',
			'--source', 'FXT.brokers.MockBrokerWithDefaults',
			'--source-account-balance', '5000',
			'--source-margin', '12.5',
			'--source-start-date', '2014-07-12 12:00:00'
		]

		parsed = self.runner.parse_arguments(options)
		self.assertEqual(parsed.source, MockBrokerWithEntity)
		self.assertEqual(parsed.source_account_balance, 5000)
		self.assertEqual(parsed.source_margin, 12.5)
		self.assertEqual(parsed.source_start_date, datetime(2014, 7, 12, 12))
"""
