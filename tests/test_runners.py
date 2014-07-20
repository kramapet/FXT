import unittest

from datetime import datetime
from FXT.runners import CliRunner

class MockBrokerWithAnnotation:
	def __init__(self, account_balance: int, margin: float, start_date: datetime):
		self.account_balance = account_balance
		self.margin = margin
		self.start_date = start_date

class MockBrokerWithDefaults:
	def __init__(self, account_balance: int, margin: float, start_date: datetime = '1989-07-20 12:00:00'):
		self.account_balance = account_balance
		self.margin = margin
		self.start_date = start_date

class MockBrokerWithoutAnnotation:
	def __init__(self, account_balance, margin, start_date):
		self.account_balance = account_balance
		self.margin = margin
		self.start_date = start_date


class MockBrokerWithEntity:
	def __init__(self, source: MockBrokerWithDefaults):
		self.source = source

class MockRenderer:
	def __init__(self):
		pass

class MockModel:
	def __init__(self, instrument: list):
		self.instrument = instrument
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

		self.runner.parse_arguments(options)

		self.assertEqual(self.runner.broker.account_balance, 2500)
		self.assertEqual(self.runner.broker.margin, 0.321)
		self.assertEqual(self.runner.broker.start_date, datetime(1989, 7, 20, 23, 0, 12))
		self.assertEqual(self.runner.model.instrument, ['USD','EUR'])

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

		self.runner.parse_arguments(options)
		self.assertEqual(self.runner.broker.account_balance, '2500')
		self.assertEqual(self.runner.broker.margin, '0.321')

	def test_parse_arguments_with_default_values(self):

		options = [
			'--broker', 'FXT.brokers.BaseBrokerDefault',
			'--model', 'FXT.models.BaseModel',
			'--renderer', 'FXT.renderers.BaseRenderer',
			'--broker-account-balance', '2500',
			'--broker-margin', '0.321',
			'--model-instrument', 'USD,EUR'
		]

		self.runner.parse_arguments(options)
		self.assertEqual(self.runner.broker.account_balance, 2500)
		self.assertEqual(self.runner.broker.margin, 0.321)
		self.assertEqual(self.runner.broker.start_date, datetime(1989, 7, 20, 12, 0, 0))

	def test_parse_arguments_with_entity(self):
		options = [
			'--broker', 'FXT.brokers.BrokerWithEntity',
			'--model', 'FXT.models.BaseModel',
			'--renderer', 'FXT.renderers.BaseRenderer',
			'--source-account-balance', '5000',
			'--source-margin', '12.5',
			'--source-start-date', '2014-07-12 12:00:00',
			'--model-instrument', 'USD,EUR'
		]

		self.runner.parse_arguments(options)
		self.assertIsInstance(self.runner.broker, MockBrokerWithEntity)
		self.assertIsInstance(self.runner.broker.source, MockBrokerWithDefaults)
		self.assertEqual(self.runner.broker.source.account_balance, 5000)
		self.assertEqual(self.runner.broker.source.margin, 12.5)
		self.assertEqual(self.runner.broker.source.start_date, datetime(2014, 7, 12, 12))

	def test_is_entity(self):
		self.assertFalse(self.runner.is_entity(int))
		self.assertFalse(self.runner.is_entity(float))
		self.assertFalse(self.runner.is_entity(str))
		self.assertFalse(self.runner.is_entity(datetime))
		self.assertFalse(self.runner.is_entity(list))
		self.assertTrue(self.runner.is_entity(MockBrokerWithAnnotation))
