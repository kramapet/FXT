#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import importlib
from datetime import datetime

from src.local_data import LocalData
from src.stat import Stat
from src.trade import Trade
from src.driver import Driver

class TestBrokerLocal():
    def __init__(self, account_balance, margin_rate, tick_source, account_currency="EUR"):
        self.account_id = None
        self.account_name = 'Local test'
        self.account_currency = account_currency
        self.margin_rate = margin_rate

        self.balance = account_balance
        self.margin_available = account_balance
        self.margin_used = 0.0

        self.open_orders = 0
        self.open_orders_list = []
        self.open_trades = 0
        self.open_trades_list = []

        self.realized_pl = 0
        self.unrealized_pl = 0

        self.tick_source = Driver.init_module_config(tick_source)

        self.stat = Stat(account_balance)
        self.last_tick = {}

        self.logger = logging.getLogger(__name__)

    def __str__(self):
        ret = "Local test broker"
        ret += "account id: " + str(self.account_id) + "\n"
        ret += "account name: " + str(self.account_name) + "\n"
        ret += "account currency: " + str(self.account_currency) + "\n"
        ret += "balance: " + str(self.balance) + "\n"
        ret += "margin available: " + str(self.margin_available) + "\n"
        ret += "margin used: " + str(self.margin_used) + "\n"
        ret += "margin rate:  " + str(self.margin_rate) + "\n"
        ret += "realized pl: " + str(self.realized_pl) + "\n"
        ret += "unrealized pl:  " + str(self.unrealized_pl) + "\n"
        return ret

    def get_tick_data(self, instrument):
        for tick in self.tick_source.get_tick_data(instrument):
            self.stat.add_tick(tick)
            self.last_tick[instrument] = tick

            # close finished sl/tp trades
            #self.open_trades_list = self.close_finished_trades(self.open_trades_list)

            yield tick

    def open(self, instrument, volume, order_type='market', expiry=None, **args):  # price=None, lower_bound=None, upper_bound=None, sl=None, tp=None, ts=None):
        if order_type == 'market':
            if volume > 0:
                open_price = self.last_tick[instrument].buy
            elif volume < 0:
                open_price = self.last_tick[instrument].sell

            trade = Trade(instrument=instrument,
                          volume=volume,
                          open_price=open_price,
                          open_datetime=self.last_tick[instrument].datetime)

            # calculate margin and convert it to the account currency if needed
            trade_margin = abs(trade.volume) * self.margin_rate
            trade_margin_converted = self.convert_to_account_currency(trade_margin, trade.instrument[0])

            if self.margin_available - trade_margin_converted < 0:
                self.logger.warning("not enough money to open the trade")
                return None
            else:
                self.margin_available -= trade_margin_converted
                self.margin_used += trade_margin_converted
                self.open_trades += 1
                self.open_trades_list.append(trade)
                return trade
        else:
            self.logger.warning("oreder_type is not 'market' - not implemented yet")
            return None

    def close(self, trade):
        if trade.volume > 0:
            close_price = self.last_tick[trade.instrument].sell
        elif trade.volume < 0:
            close_price = self.last_tick[trade.instrument].buy

        trade.close(close_price, self.last_tick[trade.instrument].datetime)

        # calculate margin and convert it to the account currency if needed
        trade_margin = abs(trade.volume) * self.margin_rate
        trade_margin_converted = self.convert_to_account_currency(trade_margin, trade.instrument[0])
        self.margin_available += trade_margin_converted
        self.margin_used -= trade_margin_converted

        # get profit in quote currency and convert it to the base currency
        quote_pl = (trade.close_rate - trade.open_rate) * trade.volume
        pl = round(self.convert_to_account_currency(quote_pl, trade.instrument[1]), 4)
        self.realized_pl += pl
        self.balance += pl
        trade.set_profit(pl)

        self.stat.add_trade(trade)
        return trade

    def convert_from_account_currency(self, volume, target_currency):
        if target_currency == self.account_currency:
            return volume
        else:
            if self.last_tick[(self.account_currency, target_currency)]:
                return volume * self.last_tick[(self.account_currency, target_currency)].buy
            else:
                tick = self.get_tick_data((self.account_currency, target_currency)).__next__()
                return volume * tick.buy

    def convert_to_account_currency(self, volume, source_currency):
        if source_currency == self.account_currency:
            return volume
        else:
            if self.last_tick[(self.account_currency, source_currency)]:
                return volume * (1.0 /self.last_tick[(self.account_currency, source_currency)].buy)
            else:
                tick = self.get_tick_data((self.account_currency, source_currency)).__next__()
                return volume * (1.0 /tick.buy)

    def close_finished_trades(self, trades):
        """
        Checks for sl/tp out. This method simulates what the real broker does and must
        be called from model after processing each new tick..
        TODO: trailing stoploss
        Arguments:
            trades list of all trades the model has opened
        Returns:
            list of trades left open
        """
        left_trades = []
        for trade in trades:
            if trade.volume > 0:
                if trade.sl:
                    if self.last_tick[trade.instrument] <= trade.sl:
                        self.close(trade)
                    else:
                        left_trades.append(trade)
                if self.tp:
                    if self.last_tick[trade.instrument] >= trade.tp:
                        self.close(trade)
                    else:
                        left_trades.append(trade)
            else:
                if trade.sl:
                    if self.last_tick[trade.instrument] >= trade.sl:
                        self.close(trade)
                    else:
                        left_trades.append(trade)
                if self.tp:
                    if self.last_tick[trade.instrument] <= trade.tp:
                        self.close(trade)
                    else:
                        left_trades.append(trade)
        return left_trades

    def get_account(self):
        """Does nothing in local implementation
        """
        None

    def get_account_information(self):
        """Does nothing in local implementation
        """
        None

    def get_open_trades(self):
        return []

class BrokerCompare(TestBrokerLocal):
    def __init__(self, real_broker):
        super().__init__(account_balance=None, margin_rate=None, tick_source=real_broker, account_currency=None)

        # set local broker parameters to be the same as the real one
        self.account_currency = self.tick_source.account_currency
        self.margin_rate = self.tick_source.margin_rate
        self.balance = self.tick_source.balance
        self.margin_available = self.tick_source.margin_available
        self.margin_used = self.tick_source.margin_used
        self.realized_pl = self.tick_source.realized_pl
        self.unrealized_pl = self.tick_source.unrealized_pl

        self.trade_dict = {}

    def __str__(self):
        self.tick_source.get_account_information()
        ret = "BROKER COMPARE OBJECT: \n"
        ret += "account currency: " + str(self.tick_source.account_currency) + "\n"
        ret += "REAL: balance: " + str(self.tick_source.balance) + "\n"
        ret += "LOCAL: balance: " + str(self.balance) + "\n"
        ret += "REAL: margin available: " + str(self.tick_source.margin_available) + "\n"
        ret += "LOCAL: margin available: " + str(self.margin_available) + "\n"
        ret += "REAL: margin used: " + str(self.tick_source.margin_used) + "\n"
        ret += "LOCAL: margin used: " + str(self.margin_used) + "\n"
        ret += "REAL: margin rate:  " + str(self.tick_source.margin_rate) + "\n"
        ret += "LOCAL: margin rate:  " + str(self.margin_rate) + "\n"
        ret += "REAL: realized pl: " + str(self.tick_source.realized_pl) + "\n"
        ret += "LOCAL: realized pl: " + str(self.realized_pl) + "\n"
        return ret

    def open(self, instrument, volume, order_type='market', expiry=None, **args):
        local = super().open(instrument, volume, order_type, expiry, **args)
        real = self.tick_source.open(instrument, volume, order_type, expiry, **args)

        self.trade_dict[local] = real
        return local

    def close(self, trade):
        real_trade = self.trade_dict[trade]
        real_trade_closed = self.tick_source.close(real_trade)
        local_trade_closed = super().close(trade)
        print("real:")
        print(real_trade_closed)
        print("local:")
        print(local_trade_closed)
        return local_trade_closed

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
